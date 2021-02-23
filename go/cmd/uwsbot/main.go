// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"path/filepath"

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
			log.Debug("bot env not set, using default")
			botEnv = "default"
		}
	}
	if err := env.Load("bot", botEnv); err != nil {
		log.Debug("%v", err)
	}

	botDir := filepath.Join(env.GetFilepath("BOTDIR"),
		filepath.FromSlash(botEnv))
	log.Debug("botdir: %s", botDir)
}
