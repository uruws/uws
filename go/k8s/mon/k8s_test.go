// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupK8sCmd string
)

func init() {
	bupK8sCmd = k8sCmd
}

func TestK8sCmd(t *testing.T) {
	IsEqual(t, k8sCmd, "get --raw /metrics", "k8sCmd")
}

func TestK8s(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	k8sCmd = "test_k8s_metrics"
	defer func() {
		kubecmd = bupKubecmd
		k8sCmd = bupK8sCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	K8s(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"),
		"text/plain; charset=utf-8", "resp content type")
}
