// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-job-stats cmd.
package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"uws/api/job/stats"
	"uws/fs"
	"uws/log"
)

func main() {
	log.Init("api-job-stats")
	env := strings.TrimSpace(os.Getenv("api_env"))
	if env == "" {
		env = "default"
	}
	statsdir := strings.TrimSpace(os.Getenv("statsdir"))
	if statsdir == "" {
		statsdir = filepath.FromSlash("/uws/var/api.job")
	}
	db_uri := strings.TrimSpace(os.Getenv("MONGO_DB_URI"))
	var fetch bool
	flag.StringVar(&statsdir, "statsdir", statsdir,
		"directory `where` to load stats info from")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.BoolVar(&fetch, "fetch", false, "fetch job stats")
	flag.Parse()

	st := stats.New()
	fn := filepath.Join(filepath.Clean(statsdir), filepath.Clean(env), "stats.json")
	lockd := filepath.Dir(fn)

	var err error
	fs.LockDir(lockd)

	if fetch {
		if db_uri == "" {
			fs.UnlockDir(lockd)
			log.Fatal("stats fetch: MONGO_DB_URI not set")
		}
		if err := st.Fetch(fn, db_uri); err != nil {
			fs.UnlockDir(lockd)
			log.Fatal("stats fetch: %s", err)
		}
		fs.UnlockDir(lockd)
	} else {
		if err := st.Load(fn); err != nil {
			fs.UnlockDir(lockd)
			log.Fatal("stats load: %s", err)
		}
		cmd := flag.Arg(0)
		if cmd == "config" {
			err = Config(st, env)
		} else {
			cmd = "report"
			err = Report(st, env)
		}
		fs.UnlockDir(lockd)
		if err != nil {
			log.Fatal("stats %s: %s", cmd, err)
		}
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
func Config(st *stats.Stats, env string) error {
	log.Debug("config: %d", st.Len())
	fmt.Printf("graph_title api jobs\n", env)
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel number of")
	fmt.Println("graph_category api")
	fmt.Println("graph_scale no")
	col := 0
	coln := ""
	for _, job := range st.List() {
		fmt.Printf("%s.label %s\n", job.ID, job.Label)
		col, coln = getColour(col)
		fmt.Printf("%s.colour %s\n", job.ID, coln)
		fmt.Printf("%s.info Number of %s jobs.\n", job.ID, job.Name)
		fmt.Printf("%s.min 0\n", job.ID)
	}
	return nil
}

// Report prints munin plugin values.
func Report(st *stats.Stats, env string) error {
	log.Debug("report: %d", st.Len())
	for _, job := range st.List() {
		fmt.Printf("%s.value %d\n", job.ID, job.Value)
	}
	return nil
}
