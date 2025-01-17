// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"fmt"

	"github.com/mattn/anko/env"
	"github.com/nsf/jsondiff"

	"uws/log"
)

type Check struct {
	assert bool
}

func newCheck() *Check {
	return &Check{}
}

func (c *Check) doAssert() {
	c.assert = true
}

func (c *Check) report(fmt string, args ...interface{}) {
	if c.assert {
		log.Fatal(fmt, args...)
	} else {
		log.Error(fmt, args...)
	}
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
	defineCkmod := func(m *env.Env, ck *Check) {
		//uwsdoc: check.http_status(resp, status_code) -> bool
		//uwsdoc: 	Checks response http status code. Returns true if it matches.
		check(m.Define("http_status", ck.HTTPStatus))
		//uwsdoc: check.http_header(resp, key, value) -> bool
		//uwsdoc: 	Checks response http header key value.
		check(m.Define("http_header", ck.HTTPHeader))
		//uwsdoc: check.json_match(resp, tag, json_string) -> bool
		//uwsdoc: 	Checks if response json body is a superset of json_string.
		//uwsdoc: 	The tag is used for error messages.
		check(m.Define("json_match", ck.JSONMatch))
		//uwsdoc: check.json_matchf(resp, tag, json_format_string, args...) -> bool
		//uwsdoc: 	Works like check.json_match but using a formatted json string.
		check(m.Define("json_matchf", ck.JSONMatchf))
	}
	defineCkmod(cm, ck)
	defineCkmod(am, assert)
}

// HTTPStatus checks http response status code.
func (c *Check) HTTPStatus(resp *Response, expect int) bool {
	if resp.r.StatusCode != expect {
		c.report("check.http_status got: %d - expect: %d", resp.r.StatusCode, expect)
		return false
	}
	return true
}

// HTTPHeader checks http response header value.
func (c *Check) HTTPHeader(resp *Response, key, expect string) bool {
	v := resp.r.Header.Get(key)
	if v != expect {
		c.report("check.http_header got: '%s' - expect: '%s'", v, expect)
		return false
	}
	return true
}

func (c *Check) readBody(r *Response) []byte {
	blob := r.readBody()
	if blob == nil {
		c.report("read response body: nil")
	}
	return blob
}

var jsondiffOptions jsondiff.Options = jsondiff.DefaultConsoleOptions()

// JSONMatch checks if response json content is a superset of expect json string.
func (c *Check) JSONMatch(resp *Response, tag string, expect []byte) bool {
	body := c.readBody(resp)
	if body == nil {
		return false
	}
	m, diff := jsondiff.Compare(body, expect, &jsondiffOptions)
	if m == jsondiff.BothArgsAreInvalidJson {
		log.Error("check.json_match error '%s': invalid json response", tag)
		c.report("check.json_match error '%s': invalid json string", tag)
		return false
	}
	if m == jsondiff.FirstArgIsInvalidJson {
		c.report("check.json_match error '%s': invalid json response", tag)
		return false
	}
	if m == jsondiff.SecondArgIsInvalidJson {
		c.report("check.json_match error '%s': invalid json string", tag)
		return false
	}
	if m == jsondiff.NoMatch {
		c.report("check.json_match failed: '%s' -> '%s'", tag, diff)
		return false
	}
	return true
}

// JSONMatchf works like JSONMatch but using a formatted json string.
func (c *Check) JSONMatchf(resp *Response, tag string, expect []byte, args ...interface{}) bool {
	return c.JSONMatch(resp, tag, []byte(fmt.Sprintf(string(expect), args...)))
}
