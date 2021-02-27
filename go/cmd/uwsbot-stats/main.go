// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsbot-stats cmd.
package main

import (
	"flag"

	"uws/bot/stats"
	"uws/env"
	"uws/log"
)

func main() {
	flag.Parse()
	log.Init("uwsbot-stats")
	if err := env.Load("bot", "stats"); err != nil {
		log.Fatal("%s", err)
	}
	stdir := env.GetFilepath("STATSDIR")
	log.Debug("stats dir: %s", stdir)
	if flag.Arg(0) == "config" {
		r, err := stats.Parse(stdir, "ALL", "ALL")
		if err != nil {
			log.Fatal("%s", err)
		}
		r.Config()
	} else {
		r, err := stats.Parse(stdir, "ALL", "ALL")
		if err != nil {
			log.Fatal("%s", err)
		}
		r.Print()
	}
}
