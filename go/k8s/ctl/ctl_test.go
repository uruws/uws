// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

const ctlDevelBindir string = "/go/src/uws/k8s/ctl/_devel/bin"

func mockCtl() {
	bindir = ctlDevelBindir
	mock.Logger()
}

func mockCtlReset() {
	bindir = "/usr/local/bin"
	mock.LoggerReset()
}

func TestGlobals(t *testing.T) {
	IsEqual(t, bindir, "/usr/local/bin", "bindir")
}

func TestCluster(t *testing.T) {
	IsEqual(t, Cluster(), "k8stest", "Cluster()")
	IsEqual(t, cluster.Name, "k8stest", "cluster.Name")
	IsEqual(t, cluster.Type, "eks", "cluster.Type")
	IsEqual(t, ClusterType(), "eks", "ClusterType()")
}

func TestMainHandler(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	MainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "index", "resp body")
}

func TestMainHandlerNotFound(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/testing"
	MainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 404, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "not found: /testing", "resp body")
}

func TestStatus(t *testing.T) {
	s := newStatus(0, "testing")
	IsEqual(t, s.Status, "ok", "status")
	IsEqual(t, s.Message, "testing", "message")
}

func TestStatusError(t *testing.T) {
	s := newStatus(99, "testing")
	IsEqual(t, s.Status, "error", "status")
	IsEqual(t, s.Message, "testing", "message")
}
