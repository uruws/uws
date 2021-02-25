// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"os"
	"path/filepath"
	"sync"

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
		wg := new(sync.WaitGroup)
		walk(wg, botEnv, botName, botDir)
		wg.Wait()
	} else {
		runScript(botDir, botRun)
	}
}

func walk(wg *sync.WaitGroup, benv, bname, bdir string) {
	rundir := filepath.Join(bdir, "run")
	log.Debug("walk %s", rundir)
	if err := filepath.Walk(rundir, dispatch(wg, benv, bname)); err != nil {
		log.Fatal("%s", err)
	}
}

func dispatch(wg *sync.WaitGroup, benv, bname string) func(filename string, st os.FileInfo, err error) error {
	return func(filename string, st os.FileInfo, err error) error {
		if err != nil {
			log.Error("dispatch: %s", err)
			return nil
		}
		if filepath.Ext(filename) == ".ank" {
			log.Print("bot dispatch: %s %s %s", benv, bname, filename)
			wg.Add(1)
			go worker(wg, benv, bname, filename)
		}
		return nil
	}
}

func worker(wg *sync.WaitGroup, benv, bname, runfn string) {
	defer wg.Done()
	log.Debug("dispatch worker: %s %s %s", benv, bname, runfn)
}

func runScript(bdir, filename string) {
	log.Print("run script %s", filename)
	e := bot.Load(bdir)
	bot.Run(e, filename)
}
