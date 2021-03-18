// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-stats cmd.
package main

import (
	"flag"
	"fmt"
	"path/filepath"

	"uws/api/stats"
	"uws/log"
)

func main() {
	log.Init("api-stats")
	var (
		statsdir string = filepath.FromSlash("/uws/var/api/stats")
		env      string = "default"
	)
	flag.StringVar(&statsdir, "statsdir", statsdir,
		"directory `where` to load stats info from")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.Parse()

	st := stats.NewReg()
	fn := filepath.Join(filepath.Clean(statsdir), filepath.Clean(env), "stats.json")
	if err := stats.Load(st, fn); err != nil {
		log.Fatal("stats load: %s", err)
	}

	var err error
	cmd := flag.Arg(0)
	if cmd == "config" {
		err = Config(st, env)
	} else {
		cmd = "report"
		err = Report(st, env)
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
	fmt.Printf("multigraph uwsapi_%s\n", env)
	fmt.Printf("graph_title bot %s api\n", env)
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel seconds")
	fmt.Println("graph_category api")
	fmt.Println("graph_scale no")
	col := 0
	coln := ""
	for _, script := range st.List() {
		fmt.Printf("%s.label %s\n", script, script)
		col, coln = getColour(col)
		fmt.Printf("%s.colour %s\n", script, coln)
		fmt.Printf("%s.min 0\n", script)
		fmt.Printf("%s.cdef %s,1000,/\n", script, script)
	}
	for _, script := range st.List() {
		fmt.Printf("multigraph uwsapi_%s.%s\n", env, script)
		fmt.Printf("graph_title bot %s api %s\n", env, script)
		fmt.Println("graph_args --base 1000 -l 0")
		fmt.Println("graph_vlabel seconds")
		fmt.Println("graph_category api")
		fmt.Println("graph_scale no")
		fmt.Println("graph_total Total elapsed time")
		inf, _ := st.Get(script)
		xlen := inf.Len()
		col = 0
		for x := 0; x < xlen; x += 1 {
			i, _ := inf.Get(x)
			fmt.Printf("f%d_%s.label /%s\n", x, i.Name, i.Label)
			col, coln = getColour(col)
			fmt.Printf("f%d_%s.colour %s\n", x, i.Name, coln)
			fmt.Printf("f%d_%s.draw AREASTACK\n", x, i.Name)
			fmt.Printf("f%d_%s.min 0\n", x, i.Name)
			fmt.Printf("f%d_%s.cdef f%d_%s,1000,/\n", x, i.Name, x, i.Name)
		}
	}
	return nil
}

// Report prints munin plugin values.
func Report(st *stats.Reg, env string) error {
	log.Debug("report: %d", st.Len())
	fmt.Printf("multigraph uwsapi_%s\n", env)
	for _, script := range st.List() {
		var took int64
		inf, _ := st.Get(script)
		xlen := inf.Len()
		for x := 0; x < xlen; x += 1 {
			i, _ := inf.Get(x)
			took += i.Took
		}
		fmt.Printf("%s.value %d\n", script, took)
	}
	for _, script := range st.List() {
		fmt.Printf("multigraph uwsapi_%s.%s\n", env, script)
		inf, _ := st.Get(script)
		xlen := inf.Len()
		for x := 0; x < xlen; x += 1 {
			i, _ := inf.Get(x)
			fmt.Printf("f%d_%s.value %d\n", x, i.Name, i.Took)
		}
	}
	return nil
}
