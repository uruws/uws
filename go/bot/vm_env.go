// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

package bot

import (
	"fmt"

	"uws/log"

	"github.com/mattn/anko/env"
)

type botEnv struct {
	*env.Env
}

func newVmEnv() *botEnv {
	return &botEnv{
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
	check(e.Define("println", fmt.Println))
	if logm, err := e.NewModule("log"); err != nil {
		log.Fatal("bot env define: %s", err)
	} else {
		check(logm.Define("fatal", log.Fatal))
		check(logm.Define("debug", log.Debug))
		check(logm.Define("error", log.Error))
	}
	return e
}
