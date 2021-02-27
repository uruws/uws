// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsbot cmd.
package main

import (
	"context"
	"flag"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"sync"
	"time"

	"uws/bot"
	"uws/bot/stats"
	"uws/env"
	"uws/log"
)

var (
	scriptTTL time.Duration = 4 * time.Minute
	scriptMax int           = 1000
)

func main() {
	var (
		botName  string
		botEnv   string
		botRun   string
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
		log.Print("init %s %s", botEnv, botName)
		st := stats.New(botEnv, botName)
		defer stats.Save(st)
		bot.Load(botDir)
		if ttl := env.Get("SCRIPT_TTL"); ttl != "" {
			if d, err := time.ParseDuration(ttl); err != nil {
				log.Error("script ttl: %s", err)
			} else {
				scriptTTL = d
			}
		}
		if max := env.Get("SCRIPT_MAX"); max != "" {
			if i, err := strconv.Atoi(max); err != nil {
				log.Error("script max: %s", err)
			} else {
				scriptMax = i
			}
		}
		ctx, cancel := context.WithTimeout(context.Background(), scriptTTL)
		defer cancel()
		wg := new(sync.WaitGroup)
		err := walk(ctx, wg, botEnv, botName, botDir, st.Dirname())
		wg.Wait()
		log.Print("end %s %s", botEnv, botName)
		if err != nil {
			st.SetError()
			log.Fatal("%s", err)
		}
	} else {
		runScript(botEnv, botName, botDir, botRun)
	}
}

func walk(ctx context.Context, wg *sync.WaitGroup, benv, bname, bdir, stdir string) error {
	rundir := filepath.Join(bdir, "run")
	log.Debug("walk %s", rundir)
	err := filepath.Walk(rundir, dispatch(ctx, wg, benv, bname, bdir, stdir))
	if err != nil {
		return err
	}
	return nil
}

func dispatch(ctx context.Context, wg *sync.WaitGroup, benv, bname, bdir, stdir string) func(filename string, st os.FileInfo, err error) error {
	scount := 0
	return func(filename string, st os.FileInfo, err error) error {
		if err != nil {
			log.Error("dispatch: %s", err)
			return nil
		}
		if filepath.Ext(filename) == ".ank" {
			fn := strings.Replace(filename, filepath.Join(bdir, "run") + string(filepath.Separator), "", 1)
			log.Debug("bot dispatch: %s %s %s", benv, bname, fn)
			if scount < scriptMax {
				wg.Add(1)
				scount += 1
				go worker(ctx, wg, scount, benv, bname, stdir, fn[:len(fn)-4]) // remove .ank from run fn
			} else {
				return log.NewError("max limit of running scripts reached: %d, refusing to dispatch another worker.", scount)
			}
		}
		return nil
	}
}

func worker(ctx context.Context, wg *sync.WaitGroup, wno int, benv, bname, stdir, runfn string) {
	defer wg.Done()
	log.Debug("dispatch worker #%d: %s %s %s", wno, benv, bname, runfn)
	st := stats.NewChild(benv, bname, stdir, runfn)
	defer stats.Save(st)
	cmd := exec.CommandContext(ctx, os.Args[0],
		"-env", benv, "-name", bname, "-run", runfn)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		st.SetError()
		log.Error("%s: %s", runfn, err)
	}
}

func runScript(benv, bname, bdir, runfn string) {
	filename := filepath.Join(bdir, "run", runfn + ".ank")
	log.Print("run script %s", filename)
	e := bot.Load(bdir)
	bot.Run(e, filename)
}
