// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ctl implements k8sctl api.
package ctl

import (
	"net/http"
	"os"

	"uws/wapp"
)

var (
	kubecmd string
	cluster string
)

func init() {
	cluster = os.Getenv("UWS_CLUSTER")
	kubecmd = os.Getenv("UWSKUBE")
	if kubecmd == "" {
		kubecmd = "/usr/local/bin/uwskube"
	}
}

func Cluster() string {
	return cluster
}

func MainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
