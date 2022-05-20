// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package api

import (
	"uws/wapp"

	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

func TestCmd(t *testing.T) {
	cmd := newCmd("testing")
	IsEqual(t, cmd.name, "testing", "cmd.name")
	IsEqual(t, len(cmd.args), 0, "cmd.args")
	IsEqual(t, cmd.String(), "/usr/local/bin/testing", "cmd.String()")
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
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	cmd.bindir = "/bin"
	outs, err := cmd.Run(r)
	IsNil(t, err, "cmd error")
	IsEqual(t, outs, "", "cmd output")
}

func TestCmdRunError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	cmd := newCmd("false")
	//~ w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	cmd.bindir = "/bin"
	outs, err := cmd.Run(r)
	IsEqual(t, outs, "", "cmd output")
	NotNil(t, err, "cmd error")
	IsEqual(t, err.Error(), "exit status 1", "cmd error message")
}

func TestCmdRunInvalidCmd(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	cmd := newCmd("testing_invalid_cmd")
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	cmd.bindir = "/bin"
	outs, err := cmd.Run(r)
	IsEqual(t, outs, "", "cmd output")
	NotNil(t, err, "cmd error")
	IsEqual(t, err.Error(),
		"fork/exec /bin/testing_invalid_cmd: no such file or directory",
		"cmd error message")
}

func TestDoExec(t *testing.T) {
	mockApi()
	defer mockApiReset()
	start := wapp.Start()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	doExec(w, r, start, "true")
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
}

func TestDoExecError(t *testing.T) {
	mockApi()
	defer mockApiReset()
	start := wapp.Start()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	doExec(w, r, start, "false")
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
}

func TestExecHandlerNoCmd(t *testing.T) {
	mockApi()
	defer mockApiReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequestPost("")
	ExecHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
}

func TestExecHandlerInvalidMethod(t *testing.T) {
	mockApi()
	defer mockApiReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	ExecHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 400, "resp status code")
}

func TestExecHandler(t *testing.T) {
	mockApi()
	defer mockApiReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequestPost("cmd=true")
	ExecHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
}
