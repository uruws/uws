// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupPodsCmd string
)

func init() {
	bupPodsCmd = podsCmd
}

func TestPodsCmd(t *testing.T) {
	IsEqual(t, podsCmd, "get pods -A -o json", "pods cmd")
}

func TestPodsCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Pods(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestPodsJSONError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	podsCmd = "test_pods_error"
	defer func() {
		kubecmd = bupKubecmd
		podsCmd = bupPodsCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Pods(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	Match(t, "^error: invalid character",
		mock.HTTPResponseString(resp), "resp body")
}

func TestPods(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	podsCmd = "test_pods"
	defer func() {
		kubecmd = bupKubecmd
		podsCmd = bupPodsCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Pods(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
}
