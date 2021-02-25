// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"path/filepath"

	"uws/bot"
	"uws/env"
	"uws/log"
)

func main() {
	var (
		botName string
		botEnv  string
		botRun  string
	)
	flag.StringVar(&botName, "name", "", "load `bot` name")
	flag.StringVar(&botEnv, "env", "", "load bot env `name`")
	flag.StringVar(&botRun, "run", "", "bot run script `filename`")

	flag.Parse()
	log.Init("uwsbot")

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

	if botName == "" {
		botName = env.Get("BOT")
		if botName == "" {
			log.Debug("bot name not set, using default")
			botName = "default"
		}
	}

	log.SetPrefix("uwsbot." + botName)

	botDir := filepath.Join(env.GetFilepath("BOTDIR"), botName)
	log.Debug("botdir: %s", botDir)

	if botRun == "" {
		bot.Load(botDir)
		//~ dispatch(botDir)
	} else {
		runScript(botDir, botRun)
	}
}

func dispatch(bdir string) {
	e := bot.Load(bdir)
	bot.Run(e, bdir + "/run/login_logout.ank")
}

func runScript(bdir, filename string) {
	e := bot.Load(bdir)
	bot.Run(e, bdir + "/run/" + filename)
}
