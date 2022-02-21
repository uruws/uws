// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8sctl util.
package main

import (
	"net/http"
	"os"

	"uws/k8s/ctl"
	"uws/log"
	"uws/wapp"
)

var (
	cluster        string
	listenAndServe func(string, http.Handler) error
	osHostname     func() (string, error)
)

func init() {
	cluster = ctl.Cluster()
	listenAndServe = http.ListenAndServe
	osHostname = os.Hostname
}

func main() {
	log.Init("k8sctl")
	log.Debug("main init")

	if cluster == "" {
		log.Fatal("UWS_CLUSTER not set")
	}
	log.Debug("cluster %s", cluster)

	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_", pingHandler)

	http.HandleFunc("/", mainHandler)

	log.Debug("serve...")
	log.Fatal("%s", listenAndServe(":4200", nil))
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if _, err := osHostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "ok\n")
	}
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if hostname, err := osHostname(); err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "ctl@%s\n", hostname)
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
