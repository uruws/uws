// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package wapp implements webapp utils.
package wapp

import (
	"net/http"
)

func Error(w http.ResponseWriter, message string, code int) {
}

func Render(w http.ResponseWriter, p *Page) {
}
