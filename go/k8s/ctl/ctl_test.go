// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)

const ctlDevelBindir string = "/go/src/uws/k8s/ctl/_devel/bin"

var (
	ctlTestServer *httptest.Server
	bupExecurl    string
)

func init() {
	bupExecurl = execurl
}

func mockCtl() {
	bindir = ctlDevelBindir
	mock.Logger()
	ctlTestServer = httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "httptest")
	}))
	execurl = ctlTestServer.URL
}

func mockCtlReset() {
	bindir = "/usr/local/bin"
	mock.LoggerReset()
	ctlTestServer.Close()
	execurl = bupExecurl
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
