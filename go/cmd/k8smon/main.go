// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements k8smon util.
package main

import (
	"fmt"
	"net/http"
	"os"

	"uws/log"
)

func main() {
	log.Init("k8smon")
	log.Debug("main init")

	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_/ping", pingHandler)

	http.HandleFunc("/", mainHandler)
	http.ListenAndServe(":2800", nil)

	log.Debug("main end")
}

func logRequest(r *http.Request, status int) {
	log.Print("%s %s %s %s - %d", r.RemoteAddr, r.Method, r.URL, r.Proto, status)
}

func writeError(w http.ResponseWriter, r *http.Request, message string, args ...interface{}) {
	http.Error(w, fmt.Sprintf(message, args...), http.StatusInternalServerError)
	logRequest(r, http.StatusInternalServerError)
}

func writeNotFound(w http.ResponseWriter, r *http.Request) {
	http.Error(w, fmt.Sprintf("%s: not found\n", r.URL.Path), http.StatusNotFound)
	logRequest(r, http.StatusNotFound)
}

func write(w http.ResponseWriter, r *http.Request, message string, args ...interface{}) {
	fmt.Fprintf(w, message, args...)
	logRequest(r, http.StatusOK)
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	write(w, r, "ok\n")
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		writeError(w, r, "ERROR: %s\n", err)
	} else {
		write(w, r, "uwsctl@%s\n", hostname)
	}
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		writeNotFound(w, r)
	} else {
		write(w, r, "index\n")
	}
}
