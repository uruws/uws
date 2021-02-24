// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"path/filepath"

	"uws/log"
)

func CheckLoad(dir string) {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("check load: %s", fn)
	e := newVmEnv()
	log.Debug("%v", e)
	if err := vmExec(e, fn); err != nil {
		log.Fatal("bot load: %s", err)
	}
}

//~ func Load(dir string) *Bot {
//~ }

//~ func Dispatch(dir string) {
//~ }

//~ func Run(b *Bot, script string) {
//~ }
