// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"encoding/json"
	"io/ioutil"

	"github.com/mattn/anko/env"

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
	defineCkmod(cm, ck)
	defineCkmod(am, assert)
}

func defineCkmod(m *env.Env, ck *Check) {
	//uwsdoc: check.http_status(resp, status_code) -> bool
	//uwsdoc: 	Checks response http status code. Returns true if it matches.
	check(m.Define("http_status", ck.HTTPStatus))
	//uwsdoc: check.http_header(resp, key, value) -> bool
	//uwsdoc: 	Checks response http header key value.
	check(m.Define("http_header", ck.HTTPHeader))
	//uwsdoc: check.json_value(resp, key, value) -> bool
	//uwsdoc: 	Checks response json body content key value.
	check(m.Define("json_value", ck.JSONValue))
	//uwsdoc: check.json_has_key(resp, key) -> bool
	//uwsdoc: 	Checks if response json body has key in its content.
	check(m.Define("json_has_key", ck.JSONHasKey))
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

type jsonResponse map[string]interface{}

func (c *Check) jsonRead(resp *Response) jsonResponse {
	if resp.body == nil {
		defer resp.r.Body.Close()
		blob, err := ioutil.ReadAll(resp.r.Body)
		if err != nil {
			c.report("json read response: %s", err)
			return nil
		}
		resp.body = blob
	}
	var body jsonResponse
	if err := json.Unmarshal(resp.body, &body); err != nil {
		c.report("json read body: %s", err)
		return nil
	}
	return body
}

// JSONValue checks response json body content value.
func (c *Check) JSONValue(resp *Response, key, expect string) bool {
	body := c.jsonRead(resp)
	if body == nil {
		return false
	}
	var got string
	if v, ok := body[key]; ok {
		got = v.(string)
	} else {
		c.report("check.json_value '%s': key not found", key)
		return false
	}
	if got != expect {
		c.report("check.json_value got: '%s' - expect: '%s'", got, expect)
		return false
	}
	return true
}

// JSONHasKey checks if response has json key name in its content.
func (c *Check) JSONHasKey(resp *Response, name string) bool {
	body := c.jsonRead(resp)
	if body == nil {
		return false
	}
	if _, ok := body[name]; !ok {
		c.report("check.json_has_key '%s': not found", name)
		return false
	}
	return true
}
