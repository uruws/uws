// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"net/http"
	"path/filepath"

	"uws/log"
)

type Bot struct {
}

func New() *Bot {
	return &Bot{}
}

func (b *Bot) Get(url string) (*http.Response, error) {
	return http.Get(url)
}

func CheckLoad(dir string) {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("check load: %s", fn)
	e := NewBotEnv()
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
