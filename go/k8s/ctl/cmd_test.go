// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

func TestCmd(t *testing.T) {
	cmd := newCmd("testing")
	IsEqual(t, cmd.name, "testing", "cmd.name")
	IsEqual(t, len(cmd.args), 0, "cmd.args")
}

func TestCmdArgs(t *testing.T) {
	cmd := newCmd("testing", "cmd", "args")
	IsEqual(t, cmd.name, "testing", "cmd.name")
	IsEqual(t, len(cmd.args), 2, "cmd.args")
	IsEqual(t, cmd.args[0], "cmd", "cmd.args[0]")
	IsEqual(t, cmd.args[1], "args", "cmd.args[1]")
}

func TestCmdRun(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	cmd := newCmd("true")
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	cmd.Run(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content-type")
	IsEqual(t, mock.HTTPResponseString(resp), `{"status":"ok","message":""}`, "resp body")
}

func TestCmdRunError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	cmd := newCmd("testing_invalid_cmd")
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	cmd.Run(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content-type")
	IsEqual(t, mock.HTTPResponseString(resp), `{"status":"error","message":"exec: \"testing_invalid_cmd\": executable file not found in $PATH"}`, "resp body")
}
