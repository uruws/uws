// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package api implements uwsapi.
package api

import (
	"net/http"
	"os"

	"uws/wapp"
)

var (
	bindir  string
)

func init() {
	bindir = os.Getenv("UWSAPI_BINDIR")
	if bindir == "" {
		bindir = "/usr/local/bin"
	}
}

func MainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
