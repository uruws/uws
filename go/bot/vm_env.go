// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

package bot

import (
	"fmt"

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

func envDefine() *env.Env {
	e := env.NewEnv()
	e.Define("println", fmt.Println)
	return e
}
