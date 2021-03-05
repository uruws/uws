// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"

	"github.com/mattn/anko/env"

	"uws/log"
)

type Check struct {
}

func newCheck() *Check {
	return &Check{}
}

func (c *Check) doAssert() {
}

func checkModule(b *Bot) {
//uwsdoc: -----
//uwsdoc: assert module:
//uwsdoc: 	Assert module shares the same methods as check module (see below).
//uwsdoc: 	But any error is reported as fatal, so the script aborts its execution.
//uwsdoc: 	In example:
//uwsdoc: 		assert.http_status(resp, status_code)
//uwsdoc: -----
//uwsdoc: check module:
	ck := newCheck()
	cm, cmerr := b.env.Env.NewModule("check")
	if cmerr != nil {
		log.Fatal("check module: %s", cmerr)
	}
	assert := newCheck()
	assert.doAssert()
	am, amerr := b.env.Env.NewModule("assert")
	if amerr != nil {
		log.Fatal("assert module: %s", amerr)
	}
	defineCkmod(cm, ck)
	defineCkmod(am, assert)
}

func defineCkmod(m *env.Env, ck *Check) {
	//uwsdoc: check.http_status(resp, status_code) -> bool
	//uwsdoc: 	Checks response http status code. Returns true if it matches.
	check(m.Define("http_status", ck.HTTPStatus))
}

func (c *Check) HTTPStatus(resp *http.Response, expect int) bool {
	if resp.StatusCode != expect {
		log.Error("check.http_status got %d - expect: %d", resp.StatusCode, expect)
		return false
	}
	return true
}
