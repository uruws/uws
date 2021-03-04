// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"

	"uws/log"
)

func libModules(b *Bot) {
	httpModule(b)
}

func httpModule(b *Bot) {
	if m, err := b.env.Env.NewModule("http"); err != nil {
		log.Fatal("http module: %s", err)
	} else {
		check(m.Define("status_ok", http.StatusOK))
	}
}
