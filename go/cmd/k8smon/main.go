// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8smon util.
package main

import (
	"net/http"
	"os"

	"uws/log"
	"uws/wapp"
)

func main() {
	log.Init("k8smon")
	log.Debug("main init")

	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_/ping", pingHandler)

	http.HandleFunc("/", mainHandler)

	log.Debug("serve...")
	log.Fatal("%s", http.ListenAndServe(":2800", nil))
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	if _, err := os.Hostname(); err != nil {
		wapp.Error(w, r, err)
	} else {
		wapp.Write(w, r, "ok\n")
	}
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		wapp.Error(w, r, err)
	} else {
		wapp.Write(w, r, "uwsctl@%s\n", hostname)
	}
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		wapp.NotFound(w, r)
	} else {
		wapp.Write(w, r, "index\n")
	}
}
