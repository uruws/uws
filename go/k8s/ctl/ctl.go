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

func (c *K8s) String() string {
	return c.Name
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
	mailx   string
	execurl string
)

func init() {
	cluster = newK8s()
	bindir = os.Getenv("UWSCTL_BINDIR")
	if bindir == "" {
		bindir = "/usr/local/bin"
	}
	mailx = os.Getenv("UWSCTL_MAILX")
	if mailx == "" {
		mailx = "/usr/bin/mailx"
	}
	execurl = os.Getenv("UWSCTL_EXECURL")
	if execurl == "" {
		execurl = "http://localhost:4200"
	}
}

func Cluster() string {
	return cluster.String()
}

func ClusterType() string {
	return cluster.Type
}

func MainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
