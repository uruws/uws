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

	var botName string
	flag.StringVar(&botName, "name", "", "load `bot` name")
	flag.Parse()

	if env.Get("ENV") == "." {
		log.Debug("set bot/default env")
		env.Load("bot/default")
		env.Set("ENV", "bot/default")
	}

	if botName == "" {
		botName = env.Get("BOT")
		if botName == "" {
			log.Debug("bot name not set, using default")
			botName = "default"
		}
	}

	botDir := filepath.Join(env.GetFilepath("BOTDIR"), botName)
	log.Debug("botdir: %s", botDir)
}
