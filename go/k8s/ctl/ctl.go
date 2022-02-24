// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ctl implements k8sctl api.
package ctl

import (
	"net/http"
	"os"

	"uws/wapp"
)

type K8s struct {
	Name string
	Type string
}

func newK8s() *K8s {
	typ := os.Getenv("UWS_CLUSTER_TYPE")
	if typ == "" {
		typ = "eks"
	}
	return &K8s{
		Name: os.Getenv("UWS_CLUSTER"),
		Type: typ,
	}
}

var (
	cluster *K8s
	bindir  string
)

func init() {
	cluster = newK8s()
	bindir = os.Getenv("UWSCTL_BINDIR")
	if bindir == "" {
		bindir = "/usr/local/bin"
	}
}

func Cluster() string {
	return cluster.Name
}

func MainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}

type ctlStatus struct {
	Status     string `json:"status"`
	StatusCode int    `json:"status_code"`
	Error      string `json:"error,omitempty"`
	Message    string `json:"message,omitempty"`
}

func newStatus(code int, msg string) *ctlStatus {
	st := "ok"
	info := msg
	errmsg := ""
	if code != 0 {
		st = "error"
		info = ""
		errmsg = msg
	}
	return &ctlStatus{
		Status: st,
		StatusCode: code,
		Error: errmsg,
		Message: info,
	}
}
