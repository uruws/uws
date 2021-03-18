// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-stats cmd.
package main

import (
	"flag"
	//~ "io/ioutil"
	//~ "os"
	"path/filepath"
	//~ "strings"

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
	fn := filepath.Join(filepath.Clean(statsdir), filepath.Clean(env), "stats")
	if err := stats.Load(st, fn); err != nil {
		log.Fatal("stats load: %s", err)
	}

	var err error
	cmd := flag.Arg(0)
	if cmd == "config" {
		err = Config(st)
	} else {
		cmd = "report"
		err = Report(st)
	}

	if err != nil {
		log.Fatal("stats %s: %s", cmd, err)
	}
}

// Config generates munin plugin config output.
func Config(st *stats.Reg) error {
	log.Debug("config: %d", st.Len())
	return nil
}

// Report prints munin plugin values.
func Report(st *stats.Reg) error {
	log.Debug("report: %d", st.Len())
	return nil
}
