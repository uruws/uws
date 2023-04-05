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
		"logs -l app.kubernetes.io/name=proxy --max-log-requests=100 --ignore-errors=true --prefix=true --timestamps=true --limit-bytes=104857600",
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

func TestNgxlogsTimeLimit35(t *testing.T) {
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

func TestNgxlogsTimeLimit50(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T00:53:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 53, "time limit minute")
	IsEqual(t, l.min_since, 45, "time limit minute since")
	IsEqual(t, l.min_until, 50, "time limit minute until")
}

func TestNgxlogsTimeLimit5(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T00:06:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 6, "time limit minute")
	IsEqual(t, l.min_since, 0, "time limit minute since")
	IsEqual(t, l.min_until, 5, "time limit minute until")
}

func TestNgxlogsTimeLimit0(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-05T00:03:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 3, "time limit minute")
	IsEqual(t, l.min_since, 55, "time limit minute since")
	IsEqual(t, l.min_until, 0, "time limit minute until")
}

func TestNgxlogsTimeLimit55(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:56:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 56, "time limit minute")
	IsEqual(t, l.min_since, 50, "time limit minute since")
	IsEqual(t, l.min_until, 55, "time limit minute until")
}

func TestNgxlogsTimeLimit45(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:46:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 46, "time limit minute")
	IsEqual(t, l.min_since, 40, "time limit minute since")
	IsEqual(t, l.min_until, 45, "time limit minute until")
}

func TestNgxlogsTimeLimit40(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:43:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 43, "time limit minute")
	IsEqual(t, l.min_since, 35, "time limit minute since")
	IsEqual(t, l.min_until, 40, "time limit minute until")
}

func TestNgxlogsTimeLimit30(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:33:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 33, "time limit minute")
	IsEqual(t, l.min_since, 25, "time limit minute since")
	IsEqual(t, l.min_until, 30, "time limit minute until")
}

func TestNgxlogsTimeLimit25(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:26:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 26, "time limit minute")
	IsEqual(t, l.min_since, 20, "time limit minute since")
	IsEqual(t, l.min_until, 25, "time limit minute until")
}

func TestNgxlogsTimeLimit20(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:23:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 23, "time limit minute")
	IsEqual(t, l.min_since, 15, "time limit minute since")
	IsEqual(t, l.min_until, 20, "time limit minute until")
}

func TestNgxlogsTimeLimit15(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:16:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 16, "time limit minute")
	IsEqual(t, l.min_since, 10, "time limit minute since")
	IsEqual(t, l.min_until, 15, "time limit minute until")
}

func TestNgxlogsTimeLimit10(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	d, err := time.Parse(time.RFC3339Nano, "2023-04-04T23:13:05.429228763Z")
	Fatal(t, IsNil(t, err, "time parse error"))
	l := ngxlogsTimeLimit(d)
	IsEqual(t, l.min, 13, "time limit minute")
	IsEqual(t, l.min_since, 5, "time limit minute since")
	IsEqual(t, l.min_until, 10, "time limit minute until")
}
