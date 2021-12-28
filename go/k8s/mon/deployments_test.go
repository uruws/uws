// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupDeployCmd string
)

func init() {
	bupDeployCmd = deployCmd
}

func TestDeployCmd(t *testing.T) {
	IsEqual(t, deployCmd, "get deployments,statefulset,daemonset -A -o json", "deploy cmd")
}

func TestDeploymentsCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Deployments(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestDeploymentsJSONError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	deployCmd = "test_deployments_error"
	defer func() {
		kubecmd = bupKubecmd
		deployCmd = bupDeployCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Deployments(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	Match(t, "^error: invalid character",
		mock.HTTPResponseString(resp), "resp body")
}

func TestDeployments(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	deployCmd = "test_deployments"
	defer func() {
		kubecmd = bupKubecmd
		deployCmd = bupDeployCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	Deployments(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
}
