// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"os"
	"path/filepath"

	"uws/bot"
	"uws/env"
	"uws/log"
)

var (
	botName string
	botEnv  string
)

func main() {
	var botRun  string
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
		walk(botDir)
	} else {
		runScript(botDir, botRun)
	}
}

func walk(bdir string) {
	rundir := filepath.Join(bdir, "run")
	log.Debug("walk %s", rundir)
	if err := filepath.Walk(rundir, dispatch); err != nil {
		log.Fatal("%s", err)
	}
}

func dispatch(filename string, st os.FileInfo, err error) error {
	if err != nil {
		log.Error("dispatch: %s", err)
		return nil
	}
	if filepath.Ext(filename) == ".ank" {
		log.Debug("dispatch: %s %s %s", botEnv, botName, filename)
	}
	return nil
}

func runScript(bdir, filename string) {
	log.Debug("run script %s", filename)
	e := bot.Load(bdir)
	bot.Run(e, filename)
}
