// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"time"

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
	IsEqual(t, ngxlogsCmd,
		"logs -l 'app.kubernetes.io/name=proxy --max-log-requests=100 --ignore-errors=true --prefix=true --timestamps=true --limit-bytes=104857600",
		"ngxlogs cmd")
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

func TestNgxlogs(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	ngxlogsCmd = "test_ngxlogs"
	defer func() {
		kubecmd = bupKubecmd
		ngxlogsCmd = bupNgxlogsCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Ngxlogs(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
}

func TestNgxlogsTimeLimit(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T04:36:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.unix, int64(1680669365), "time limit unix representation")
	IsEqual(t, l.min, 36, "time limit minute")
	IsEqual(t, l.min_since, 30, "time limit minute since")
	IsEqual(t, l.min_until, 35, "time limit minute until")
}

func TestNgxlogsTimeLimit2(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T00:06:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.unix, int64(1680653165), "time limit unix representation")
	IsEqual(t, l.min, 6, "time limit minute")
	IsEqual(t, l.min_since, 0, "time limit minute since")
	IsEqual(t, l.min_until, 5, "time limit minute until")
}

func TestNgxlogsTimeLimit3(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T00:03:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.unix, int64(1680652985), "time limit unix representation")
	IsEqual(t, l.min, 3, "time limit minute")
	IsEqual(t, l.min_since, 55, "time limit minute since")
	IsEqual(t, l.min_until, 0, "time limit minute until")
}

func TestNgxlogsTimeLimit4(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:56:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.unix, int64(1680652565), "time limit unix representation")
	IsEqual(t, l.min, 56, "time limit minute")
	IsEqual(t, l.min_since, 50, "time limit minute since")
	IsEqual(t, l.min_until, 55, "time limit minute until")
}
