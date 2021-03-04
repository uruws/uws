// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"

	"uws/log"
)

type Check struct {
}

func newCheck() *Check {
	return &Check{}
}

func checkModule(b *Bot) {
//uwsdoc: --------------------------------------------------------------------------------
//uwsdoc: check module:
	ck := newCheck()
	if m, err := b.env.Env.NewModule("check"); err != nil {
		log.Fatal("check module: %s", err)
	} else {
	//uwsdoc: check.http_status(resp, status_code) -> bool
	//uwsdoc: 	Checks response http status code. Returns true if it matches.
		check(m.Define("http_status", ck.HTTPStatus))
	}
}

func (c *Check) HTTPStatus(resp *http.Response, expect int) bool {
	if resp.StatusCode != expect {
		log.Error("check.http_status got %d - expect: %d", resp.StatusCode, expect)
		return false
	}
	return true
}
