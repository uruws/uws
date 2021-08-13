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

	log.Debug("serve...")
	log.Fatal("%s", http.ListenAndServe(":2800", nil))
}

func logRequest(r *http.Request, status, size int) {
	log.Print("%s %s %s %d %d", r.RemoteAddr, r.Method, r.URL, status, size)
}

func writeError(w http.ResponseWriter, r *http.Request, err error) {
	log.Error("%s", err)
	http.Error(w, fmt.Sprintf("error: %s\n", err), http.StatusInternalServerError)
	logRequest(r, http.StatusInternalServerError, len("error: \n") + len(err.Error()))
}

func writeNotFound(w http.ResponseWriter, r *http.Request) {
	http.Error(w, fmt.Sprintf("not found: %s\n", r.URL.Path), http.StatusNotFound)
	logRequest(r, http.StatusNotFound, len("not found: \n") + len(r.URL.Path))
}

func write(w http.ResponseWriter, r *http.Request, message string, args ...interface{}) {
	n, err := fmt.Fprintf(w, message, args...)
	if err != nil {
		log.Error("%s %s: %s", r.Method, r.URL, err)
	} else {
		logRequest(r, http.StatusOK, n)
	}
}

func healthzHandler(w http.ResponseWriter, r *http.Request) {
	if _, err := os.Hostname(); err != nil {
		writeError(w, r, err)
	} else {
		write(w, r, "ok\n")
	}
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		writeError(w, r, err)
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
