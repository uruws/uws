// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package wapp implements webapp utils.
package wapp

import (
	"fmt"
	"net/http"

	"uws/log"
)

func logRequest(r *http.Request, status, size int) {
	log.Print("%s %s %s %d %d", r.RemoteAddr, r.Method, r.URL, status, size)
}

func ServeStatic(dir string) {
	http.Handle("/static/",
		http.StripPrefix("/static/", http.FileServer(http.Dir(dir))))
}

func Error(w http.ResponseWriter, r *http.Request, err error) {
	log.Error("%s", err)
	http.Error(w, fmt.Sprintf("error: %s", err), http.StatusInternalServerError)
	logRequest(r, http.StatusInternalServerError, len("error: \n") + len(err.Error()))
}

func NotFound(w http.ResponseWriter, r *http.Request) {
	http.Error(w, fmt.Sprintf("not found: %s", r.URL.Path), http.StatusNotFound)
	logRequest(r, http.StatusNotFound, len("not found: \n") + len(r.URL.Path))
}

func Write(w http.ResponseWriter, r *http.Request, message string, args ...interface{}) {
	n, err := fmt.Fprintf(w, message, args...)
	if err != nil {
		log.Error("%s %s: %s", r.Method, r.URL, err)
	} else {
		logRequest(r, http.StatusOK, n)
	}
}
