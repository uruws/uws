// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package bot implements a monitoring bot.
package bot

import (
	"context"
	"net/url"
	"path/filepath"

	"uws/bot/stats"
	"uws/config/appcfg"
	"uws/log"
)

const version string = '0.1'

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
	cfg   *appcfg.Config
}

func New(benv, bname string) *Bot {
	return &Bot{
		benv:  benv,
		bname: bname,
		env:   newBotEnv(),
		sess:  newBotSession(),
		cfg:   appcfg.New(),
	}
}

func botModule(b *Bot) {
	//uwsdoc: -----
	//uwsdoc: bot module:
	if botm, err := b.env.Env.NewModule("bot"); err != nil {
		log.Fatal("bot module: %s", err)
	} else {
		//uwsdoc: bot.set_base_url(url)
		//uwsdoc: 	Sets the base url for future requests.
		check(botm.Define("set_base_url", b.SetBaseURL))
		//uwsdoc: bot.login(url)
		//uwsdoc: 	Logs in to url using configured email/pass credentials.
		//uwsdoc: 	It also sets the auth session headers used to authenticate
		//uwsdoc: 	future requests.
		check(botm.Define("login", b.Login))
		//uwsdoc: bot.logout(url)
		//uwsdoc: 	Logs out from url using auth session (if any).
		check(botm.Define("logout", b.Logout))
		//uwsdoc: bot.get(url) -> resp
		//uwsdoc: 	Returns a response from a GET request to url.
		check(botm.Define("get", b.Get))
		//uwsdoc: bot.post_form(url, values) -> resp
		//uwsdoc: 	Returns a response from a POST (form-urlencoded) request to url.
		check(botm.Define("post_form", b.PostForm))
	}
}

func cfgModule(b *Bot, cfgdir string) {
	//uwsdoc: -----
	//uwsdoc: config module:
	if m, err := b.env.Env.NewModule("config"); err != nil {
		log.Fatal("config module: %s", err)
	} else {
		b.cfg.SetConfigDir(cfgdir)
		fn := b.benv + ".yml"
		if err := b.cfg.Load(fn); err != nil {
			log.Fatal("config module load file: %s", err)
		}
		log.Debug("%s config loaded", fn)
		//uwsdoc: config.get(key) -> string
		//uwsdoc: 	Returns the config key value.
		check(m.Define("get", b.cfg.Get))
	}
}

func Load(ctx context.Context, benv, bname, dir string) *Bot {
	fn := filepath.Join(dir, "bot.ank")
	log.Debug("load: %s", fn)
	b := New(benv, bname)
	botModule(b)
	cfgModule(b, filepath.Join(dir, "config"))
	checkModule(b)
	libModules(b)
	if err := vmExec(ctx, b, fn); err != nil {
		log.Fatal("bot load: %s", err)
	}
	return b
}

func Run(ctx context.Context, b *Bot, bdir, stdir, runfn string) error {
	script := filepath.Join(bdir, "run", runfn+".ank")
	log.Debug("bot run: %s", script)
	b.setStats(stdir, runfn)
	if err := vmExec(ctx, b, script); err != nil {
		log.Debug("bot run: %s", err)
		return err
	}
	return nil
}

func (b *Bot) setStats(stdir, runfn string) {
	b.stats = newScriptStats(b.benv, b.bname, stdir, runfn)
}

// SetBaseUrl sets the base url for future requests.
func (b *Bot) SetBaseURL(uri string) {
	log.Debug("set base url %s", uri)
	if err := b.sess.SetBaseURL(uri); err != nil {
		log.Fatal("bot.set_base_url %s: %s", uri, err)
	}
}

// Login logs in to url using configured email/pass credentials.
func (b *Bot) Login(uri string) {
	log.Debug("login %s", uri)
	st := b.stats.New("LOGIN", uri)
	defer b.stats.Save(st)
	if err := b.sess.Login(uri); err != nil {
		log.Fatal("bot.login %s: %s", uri, err)
	}
}

// Logout logs out from url using auth headers from Login.
func (b *Bot) Logout(uri string) {
	log.Debug("logout %s", uri)
	st := b.stats.New("LOGOUT", uri)
	defer b.stats.Save(st)
	if err := b.sess.Logout(uri); err != nil {
		log.Fatal("bot.logout %s: %s", uri, err)
	}
}

// Get returns a response from a GET request to uri.
func (b *Bot) Get(uri string) *Response {
	log.Debug("get %s", uri)
	st := b.stats.New("GET", uri)
	defer b.stats.Save(st)
	resp, err := b.sess.Get(uri)
	if err != nil {
		log.Fatal("bot.get %s: %s", uri, err)
	}
	return newResponse(resp)
}

// PostForm returns a response from a POST request to url.
func (b *Bot) PostForm(uri string, vals url.Values) *Response {
	log.Debug("get %s", uri)
	st := b.stats.New("POST", uri)
	defer b.stats.Save(st)
	resp, err := b.sess.PostForm(uri, vals)
	if err != nil {
		log.Fatal("bot.post %s: %s", uri, err)
	}
	return newResponse(resp)
}
