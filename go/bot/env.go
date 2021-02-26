// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"fmt"

	"uws/log"

	"github.com/mattn/anko/env"
)

type BotEnv struct {
	*env.Env
}

func NewBotEnv() *BotEnv {
	return &BotEnv{
		Env: envDefine(),
	}
}

func check(err error) {
	if err != nil {
		log.Fatal("bot env define: %s", err)
	}
}

func envDefine() *env.Env {
	e := env.NewEnv()
	if logm, err := e.NewModule("log"); err != nil {
		log.Fatal("bot env log module: %s", err)
	} else {
		check(logm.Define("fatal", log.Fatal))
		check(logm.Define("debug", log.Debug))
		check(logm.Define("error", log.Error))
		check(logm.Define("warn", log.Warn))
		check(logm.Define("print", log.Print))
	}
	b := New()
	newModule(b, e)
	return e
}
