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
	kubecmd string
	cluster *K8s
)

func init() {
	cluster = newK8s()
	kubecmd = os.Getenv("UWSKUBE")
	if kubecmd == "" {
		kubecmd = "/usr/local/bin/uwskube"
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
