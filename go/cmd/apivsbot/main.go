// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements apivsbot cmd util.
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"uws/api/stats"
	"uws/fs"
	"uws/log"

	botstats "uws/bot/stats"
)

func main() {
	log.Init("apivsbot")
	env := strings.TrimSpace(os.Getenv("api_env"))
	if env == "" {
		env = "default"
	}
	statsdir := strings.TrimSpace(os.Getenv("statsdir"))
	if statsdir == "" {
		statsdir = filepath.FromSlash("/uws/var/api/stats")
	}
	flag.StringVar(&statsdir, "statsdir", statsdir,
		"directory from `where` to load api stats info")
	botsdir := strings.TrimSpace(os.Getenv("botsdir"))
	if botsdir == "" {
		botsdir = filepath.FromSlash("/uws/var/uwsbot/stats")
	}
	flag.StringVar(&botsdir, "botsdir", botsdir,
		"directory from `where` to load bots stats info")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.Parse()

	st := stats.NewReg()
	fn := filepath.Join(filepath.Clean(statsdir), filepath.Clean(env), "stats.json")
	lockd := filepath.Dir(fn)
	fs.LockDir(lockd)
	if err := stats.Load(st, fn); err != nil {
		fs.UnlockDir(lockd)
		log.Fatal("api stats load: %s", err)
	}
	fs.UnlockDir(lockd)

	var (
		err error
		bst *botstats.Report
	)

	cmd := flag.Arg(0)
	if cmd == "config" {
		err = Config(st, env)
	} else {
		cmd = "report"
		bst, err = botstats.Parse(botsdir, env, "api")
		if err != nil {
			log.Fatal("bot stats load: %s", err)
		}
		err = Report(st, env, bst)
	}

	if err != nil {
		log.Fatal("stats %s: %s", cmd, err)
	}
}

func getColour(i int) (int, string) {
	if i > 28 {
		i = 0
	}
	n := fmt.Sprintf("COLOUR%d", i)
	return i+1, n
}

// Config generates munin plugin config output.
func Config(st *stats.Reg, env string) error {
	log.Debug("config: %d", st.Len())
	for _, script := range st.List() {
		inf, _ := st.Get(script)
		fmt.Printf("multigraph apivsbot_%s_%s\n", env, script)
		fmt.Printf("graph_title api vs bot: %s %s\n", env, inf.Name)
		fmt.Println("graph_args --base 1000 -l 0")
		fmt.Println("graph_vlabel seconds")
		fmt.Println("graph_category api")
		fmt.Println("graph_scale no")
		fmt.Println("graph_total Total elapsed time")
		fmt.Println("api.label api")
		fmt.Println("api.colour COLOUR0")
		fmt.Println("api.min 0")
		fmt.Println("api.cdef api,1000,/")
		fmt.Println("bot.label bot")
		fmt.Println("bot.colour COLOUR1")
		fmt.Println("bot.min 0")
		fmt.Println("bot.cdef bot,1000,/")
	}
	return nil
}

// Report prints munin plugin values.
func Report(st *stats.Reg, env string, bst *botstats.Report) error {
	log.Debug("report: %d %d", st.Len(), bst.Len())
	r := bst.Get()
	for _, script := range st.List() {
		var took int64
		fmt.Printf("multigraph apivsbot_%s_%s\n", env, script)
		inf, _ := st.Get(script)
		xlen := inf.Len()
		for x := 0; x < xlen; x += 1 {
			i, _ := inf.Get(x)
			took += i.Took
		}
		fmt.Printf("api.value %d\n", took)
		if v, ok := r[script]; ok {
			fmt.Printf("bot.value %d\n", v)
		} else {
			fmt.Println("bot.value U")
		}
	}
	return nil
}
