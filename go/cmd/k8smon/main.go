// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8smon util.
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_/ping", pingHandler)
	http.HandleFunc("/", mainHandler)
	http.ListenAndServe(":2800", nil)
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "ok")
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		fmt.Fprintf(w, "ERROR: %s\n", err)
	} else {
		fmt.Fprintf(w, "uwsctl@%s\n", hostname)
	}
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "index")
}
