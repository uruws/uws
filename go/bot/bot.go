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

func (b *Bot) Login(url string) *BotSession {
	return Login(url)
}

func (b *Bot) Get(url string) (*http.Response, error) {
	return http.Get(url)
}

func Load(dir string) *BotEnv {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("check load: %s", fn)
	e := NewBotEnv()
	if err := vmExec(e, fn); err != nil {
		log.Fatal("bot check load: %s", err)
	}
	return e
}

func Run(e *BotEnv, script string) {
	if err := vmExec(e, script); err != nil {
		log.Fatal("bot run: %s", err)
	}
}
