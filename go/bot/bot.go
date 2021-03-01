// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"net/http"
	"path/filepath"

	"uws/log"
)

type Bot struct {
	benv  string
	bname string
	env   *botEnv
	sess  *botSession
}

func New(benv, bname string) *Bot {
	return &Bot{
		benv: benv,
		bname: bname,
		env:   newBotEnv(),
		sess:  newBotSession(),
	}
}

func Load(benv, bname, dir string) *Bot {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("load: %s", fn)
	b := New(benv, bname)
	envModule(b)
	if err := vmExec(b, fn); err != nil {
		log.Fatal("bot check load: %s", err)
	}
	envModule(b)
	return b
}

func Run(b *Bot, script string) {
	if err := vmExec(b, script); err != nil {
		log.Fatal("bot run: %s", err)
	}
}

func envModule(b *Bot) {
	if botm, err := b.env.Env.NewModule("bot"); err != nil {
		log.Fatal("bot env module: %s", err)
	} else {
		check(botm.Define("set_base_url", b.SetBaseURL))
		check(botm.Define("login", b.Login))
		check(botm.Define("logout", b.Logout))
		check(botm.Define("get", b.Get))
	}
}

func (b *Bot) SetBaseURL(url string) {
	log.Debug("set base url %s", url)
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

func (b *Bot) Logout(url string) {
	log.Debug("logout %s", url)
	if err := b.sess.Logout(url); err != nil {
		log.Fatal("bot.logout %s: %s", url, err)
	}
}

func (b *Bot) Get(url string) *http.Response {
	resp, err := b.sess.Get(url)
	if err != nil {
		log.Fatal("bot.get %s: %s", url, err)
	}
	return resp
}
