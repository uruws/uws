// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"

	"uws/env"
	"uws/log"
)

func main() {
	log.Init("uwsbot")

	var botEnv string
	flag.StringVar(&botEnv, "bot", "", "load bot `env`")
	flag.Parse()

	if botEnv == "" {
		botEnv = env.Get("BOT")
		if botEnv == "" {
			log.Fatal("bot env not set")
		}
	}
	if err := env.Load("bot", botEnv); err != nil {
		log.Debug("%v", err)
	}
	botDir := env.GetFilepath("BOTDIR", botEnv)
	log.Debug("botdir: %s", botDir)
}
