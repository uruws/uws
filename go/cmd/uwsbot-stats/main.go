// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsbot-stats cmd.
package main

import (
	"flag"

	//~ "uws/bot/stats"
	"uws/env"
	"uws/log"
)

func main() {
	var (
		botEnv   string
	)
	flag.StringVar(&botEnv, "env", "", "load bot env `name`")

	flag.Parse()
	log.Init("uwsbot-stats")

	if botEnv == "" {
		if env.Get("ENV") == "." {
			log.Debug("set bot/default env")
			env.Load("bot/default")
			env.Set("ENV", "bot/default")
			botEnv = "bot/default"
		}
	} else {
		log.Debug("set %s env", botEnv)
		if err := env.Load(botEnv); err != nil {
			log.Fatal("%s", err)
		}
		env.Set("ENV", botEnv)
	}

	stdir := env.GetFilepath("STATSDIR")
	log.Debug("stats dir: %s", stdir)
}
