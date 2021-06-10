// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ca implements uwsca webapp handlers.
package ca

import (
	"net/http"

	"uws/log"
	"uws/wapp"
)

func Index(w http.ResponseWriter, r *http.Request) {
	log.Debug("index")
	p := wapp.NewPage("ca/index.html")
	p.Title = "uwsca"
	wapp.Render(w, p)
}
