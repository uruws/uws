// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupNodesCmd string
)

func init() {
	bupNodesCmd = nodesCmd
}

func TestNodesCmd(t *testing.T) {
	IsEqual(t, nodesCmd, "get nodes -o json", "nodes cmd")
}

func TestNodesCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Nodes(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestNodesJSONError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	nodesCmd = "test_nodes_error"
	defer func() {
		kubecmd = bupKubecmd
		nodesCmd = bupNodesCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Nodes(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	Match(t, "^error: invalid character",
		mock.HTTPResponseString(resp), "resp body")
}

func TestNodes(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	nodesCmd = "test_nodes"
	defer func() {
		kubecmd = bupKubecmd
		nodesCmd = bupNodesCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Nodes(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
}
