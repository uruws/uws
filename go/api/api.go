// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package api implements uwsapi.
package api

import (
	"net/http"
	"os"
	"strconv"

	"uws/wapp"
)

var (
	bindir string
	cmdttl int
)

func init() {
	bindir = os.Getenv("UWSAPI_BINDIR")
	if bindir == "" {
		bindir = "/usr/local/bin"
	}
	cmdttlString := os.Getenv("UWSAPI_CMDTTL")
	if cmdttlString == "" {
		cmdttlString = "/usr/local/bin"
	}
	cmdttlInt, _ := strconv.ParseInt(cmdttlString, 10, 0)
	cmdttl = int(cmdttlInt)
	if cmdttl <= 0 {
		cmdttl = 300 // 5 minutes
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
