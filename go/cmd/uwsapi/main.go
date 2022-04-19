// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsapi web service.
package main

import (
	"fmt"
	"net/http"
	"os"

	"uws/api"
	"uws/log"
	"uws/wapp"
)

var (
	listenAndServe func(string, http.Handler) error
	osHostname     func() (string, error)
)

func init() {
	listenAndServe = http.ListenAndServe
	osHostname = os.Hostname
}

func main() {
	log.Init("uwsapi")
	log.Print("init...")

	http.HandleFunc("/_/healthz", healthzHandler)
	http.HandleFunc("/_", pingHandler)

	http.HandleFunc("/exec", api.ExecHandler)
	http.HandleFunc("/", api.MainHandler)

	log.Print("listen...")
	log.Fatal("%s", listenAndServe(fmt.Sprintf(":%d", api.Port), nil))
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
