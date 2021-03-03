// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"context"
	"net/http"
	"net/url"
	"path/filepath"

	"uws/bot/stats"
	"uws/log"
)

type scriptStats struct {
	benv  string
	bname string
	stdir string
	runfn string
}

func newScriptStats(benv, bname, stdir, runfn string) *scriptStats {
	return &scriptStats{benv, bname, stdir, runfn}
}

func (s *scriptStats) New(args ...string) *stats.Stats {
	return stats.NewScript(s.benv, s.bname, s.stdir, s.runfn, args...)
}

func (s *scriptStats) Save(st *stats.Stats) {
	stats.Save(st)
}

type Bot struct {
	benv  string
	bname string
	env   *botEnv
	sess  *botSession
	stats *scriptStats
}

func New(benv, bname string) *Bot {
	return &Bot{
		benv:  benv,
		bname: bname,
		env:   newBotEnv(),
		sess:  newBotSession(),
	}
}

func Load(ctx context.Context, benv, bname, dir string) *Bot {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("load: %s", fn)
	b := New(benv, bname)
	envModule(b)
	if err := vmExec(ctx, b, fn); err != nil {
		log.Fatal("bot check load: %s", err)
	}
	return b
}

func Run(ctx context.Context, b *Bot, bdir, stdir, runfn string) {
	script := filepath.Join(bdir, "run", runfn+".ank")
	log.Debug("bot run: %s", script)
	b.setStats(stdir, runfn)
	if err := vmExec(ctx, b, script); err != nil {
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

func (b *Bot) setStats(stdir, runfn string) {
	b.stats = newScriptStats(b.benv, b.bname, stdir, runfn)
}

func (b *Bot) SetBaseURL(uri string) {
	log.Debug("set base url %s", uri)
	if err := b.sess.SetBaseURL(uri); err != nil {
		log.Fatal("bot.set_base_url %s: %s", uri, err)
	}
}

func (b *Bot) Login(uri string) {
	log.Debug("login %s", uri)
	st := b.stats.New("LOGIN", uri)
	defer b.stats.Save(st)
	if err := b.sess.Login(uri); err != nil {
		log.Fatal("bot.login %s: %s", uri, err)
	}
}

func (b *Bot) Logout(uri string) {
	log.Debug("logout %s", uri)
	st := b.stats.New("LOGOUT", uri)
	defer b.stats.Save(st)
	if err := b.sess.Logout(uri); err != nil {
		log.Fatal("bot.logout %s: %s", uri, err)
	}
}

func (b *Bot) Get(uri string) *http.Response {
	log.Debug("get %s", uri)
	st := b.stats.New("GET", uri)
	defer b.stats.Save(st)
	resp, err := b.sess.Get(uri)
	if err != nil {
		log.Fatal("bot.get %s: %s", uri, err)
	}
	return resp
}

func (b *Bot) PostForm(uri string, vals url.Values) *http.Response {
	log.Debug("get %s", uri)
	st := b.stats.New("POST", uri)
	defer b.stats.Save(st)
	resp, err := b.sess.PostForm(uri, vals)
	if err != nil {
		log.Fatal("bot.post %s: %s", uri, err)
	}
	return resp
}
