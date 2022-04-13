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
	Port   int
)

func configure() {
	bindir = os.Getenv("UWSAPI_BINDIR")
	if bindir == "" {
		bindir = "/usr/local/bin"
	}
	cmdttlString := os.Getenv("UWSAPI_CMDTTL")
	if cmdttlString == "" {
		cmdttlString = "300"
	}
	cmdttlInt, _ := strconv.ParseInt(cmdttlString, 10, 0)
	cmdttl = int(cmdttlInt)
	if cmdttl <= 0 {
		cmdttl = 300 // 5 minutes
	}
	portString := os.Getenv("UWSAPI_PORT")
	if portString == "" {
		portString = "3800"
	}
	portInt, _ := strconv.ParseInt(portString, 10, 0)
	Port = int(portInt)
	if Port <= 0 {
		Port = 3800
	}
}

func init() {
	configure()
}

func MainHandler(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	if r.URL.Path != "/" {
		wapp.NotFound(w, r, start)
	} else {
		wapp.Write(w, r, start, "index\n")
	}
}
