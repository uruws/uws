// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupNgxlogsCmd string
)

func init() {
	bupNgxlogsCmd = ngxlogsCmd
}

func TestNgxlogsCmd(t *testing.T) {
	IsEqual(t, ngxlogsCmd, "logs -l 'app.kubernetes.io/name=proxy --max-log-requests 100 --ignore-errors=true --prefix=true --timestamps=true", "ngxlogs cmd")
}

func TestNgxlogsCmdError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Ngxlogs(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestNgxlogsJSONError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	ngxlogsCmd = "test_ngxlogs_error"
	defer func() {
		kubecmd = bupKubecmd
		ngxlogsCmd = bupNgxlogsCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Ngxlogs(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	Match(t, "^error: invalid character",
		mock.HTTPResponseString(resp), "resp body")
}
