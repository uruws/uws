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

func getScriptTtl() time.Duration {
	var err error
	d := scriptTTL
	if ttl := env.Get("SCRIPT_TTL"); ttl != "" {
		if d, err = time.ParseDuration(ttl); err != nil {
			log.Error("get script ttl: %s", err)
		}
	}
	return d
}

func getScriptMax() int {
	var err error
	i := scriptMax
	if max := env.Get("SCRIPT_MAX"); max != "" {
		if i, err = strconv.Atoi(max); err != nil {
			log.Error("get script max: %s", err)
		}
	}
	return i
}

func main() {
	var (
		botName  string
		botEnv   string
		botRun   string
		botStats string
	)
	flag.StringVar(&botName, "name", "", "load `bot` name")
	flag.StringVar(&botEnv, "env", "", "load bot env `name`")
	flag.StringVar(&botRun, "run", "", "bot run script `filename`")
	flag.StringVar(&botStats, "stats", "", "bot stats `dirname`")

	flag.Parse()
	log.Init("uwsbot")

	if botEnv == "" {
		if env.Get("ENV") == "." {
			log.Debug("set bot/default env")
			if err := env.Load("bot/default"); err != nil {
				log.Error("%s", err)
			}
			env.Set("ENV", "default")
			botEnv = "default"
		}
	} else {
		log.Debug("set %s env", botEnv)
		if err := env.Load("bot", botEnv); err != nil {
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
		ctx, cancel := context.WithTimeout(context.Background(), getScriptTtl())
		defer cancel()
		bot.Load(ctx, botEnv, botName, botDir)
		wg := new(sync.WaitGroup)
		err := walk(ctx, wg, botEnv, botName, botDir, st.Dirname())
		wg.Wait()
		log.Print("end %s %s", botEnv, botName)
		if err != nil {
			st.SetError()
			log.Fatal("%s", err)
			os.RemoveAll(st.Dirname())
		}
	} else {
		runScript(botEnv, botName, botDir, botStats, botRun)
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
	runmax := getScriptMax()
	scount := 0
	return func(filename string, st os.FileInfo, err error) error {
		if err != nil {
			log.Error("dispatch: %s", err)
			return nil
		}
		if filepath.Ext(filename) == ".ank" {
			fn := strings.Replace(filename, filepath.Join(bdir, "run")+string(filepath.Separator), "", 1)
			log.Debug("bot dispatch: %s %s %s", benv, bname, fn)
			if scount < runmax {
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
		"-env", benv, "-name", bname, "-stats", stdir, "-run", runfn)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		st.SetError()
		log.Error("%s: %s", runfn, err)
	}
}

func runScript(benv, bname, bdir, stdir, runfn string) {
	log.Print("run script: %s %s", bdir, runfn)
	ctx, cancel := context.WithTimeout(context.Background(), getScriptTtl())
	defer cancel()
	b := bot.Load(ctx, benv, bname, bdir)
	bot.Run(ctx, b, bdir, stdir, runfn)
}
