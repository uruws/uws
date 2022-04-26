// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package api

import (
	"os"
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)

const apiDevelBindir string = "/go/src/uws/api/_devel/bin"

func mockApi() {
	bindir = apiDevelBindir
	mock.Logger()
}

func mockApiReset() {
	bindir = "/usr/local/bin"
	mock.LoggerReset()
}

func TestGlobals(t *testing.T) {
	IsEqual(t, bindir, "/usr/local/bin", "bindir")
	IsEqual(t, cmdttl, 300, "cmdttl")
	IsEqual(t, Port, 3800, "Port")
}

func TestConfigure(t *testing.T) {
	// cmdttl
	os.Setenv("UWSAPI_CMDTTL", "0")
	configure()
	IsEqual(t, cmdttl, 300, "cmdttl")
	// Port
	os.Setenv("UWSAPI_PORT", "-1")
	configure()
	IsEqual(t, Port, 3800, "Port")
}

func TestMainHandler(t *testing.T) {
	mockApi()
	defer mockApiReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	MainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "index", "resp body")
}

func TestMainHandlerNotFound(t *testing.T) {
	mockApi()
	defer mockApiReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/testing"
	MainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 404, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "not found: /testing", "resp body")
}
