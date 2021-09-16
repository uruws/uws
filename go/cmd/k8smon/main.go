// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8smon util.
package main

import (
	"net/http"
	"os"

	"uws/k8s/mon"
	"uws/log"
	"uws/wapp"
)

func main() {
	log.Init("k8smon")
	log.Debug("main init")

	if mon.Cluster() == "" {
		log.Fatal("UWS_CLUSTER not set")
	} else {
		log.Debug("cluster %s", mon.Cluster())
	}

	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_/ping", pingHandler)

	http.HandleFunc("/kube/nodes", mon.Nodes)
	http.HandleFunc("/kube/deployments", mon.Deployments)
	http.HandleFunc("/kube/pods", mon.Pods)

	http.HandleFunc("/", mainHandler)

	log.Debug("serve...")
	log.Fatal("%s", http.ListenAndServe(":2800", nil))
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if _, err := os.Hostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "ok\n")
	}
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if hostname, err := os.Hostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "uwsctl@%s\n", hostname)
	}
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
