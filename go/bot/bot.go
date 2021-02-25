// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"net/http"
	"path/filepath"

	"uws/log"
)

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

type Bot struct {
	sess *botSession
}

func New() *Bot {
	return &Bot{sess: new(botSession)}
}

func (b *Bot) SetBaseURL(url string) {
	log.Debug("set base url %s")
	if err := b.sess.SetBaseURL(url); err != nil {
		log.Fatal("bot.set_base_url %s: %s", url, err)
	}
}

func (b *Bot) Login(url string) {
	log.Debug("login %s", url)
	if err := b.sess.Login(url); err != nil {
		log.Fatal("bot.login %s: %s", url, err)
	}
}

func (b *Bot) Get(url string) *http.Response {
	resp, err := http.Get(url)
	if err != nil {
		log.Fatal("bot.get %s: %s", url, err)
	}
	return resp
}
