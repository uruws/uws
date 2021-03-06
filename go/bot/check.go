// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"encoding/json"
	"io/ioutil"
	"net/http"

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
func (c *Check) HTTPStatus(resp *http.Response, expect int) bool {
	if resp.StatusCode != expect {
		c.report("check.http_status got: %d - expect: %d", resp.StatusCode, expect)
		return false
	}
	return true
}

// HTTPHeader checks http response header value.
func (c *Check) HTTPHeader(resp *http.Response, key, expect string) bool {
	v := resp.Header.Get(key)
	if v != expect {
		c.report("check.http_header got: '%s' - expect: '%s'", v, expect)
		return false
	}
	return true
}

type jsonResponse map[string]interface{}

func (c *Check) jsonRead(resp *http.Response) jsonResponse {
	defer resp.Body.Close()
	blob, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Error("json read response: %s", err)
		return nil
	}
	var body jsonResponse
	if err := json.Unmarshal(blob, &body); err != nil {
		log.Error("json read body: %s", err)
		return nil
	}
	return body
}

// JSONValue checks response json body content value.
func (c *Check) JSONValue(resp *http.Response, key, expect string) bool {
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
func (c *Check) JSONHasKey(resp *http.Response, name string) bool {
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
