// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package wapp implements webapp utils.
package wapp

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"

	"uws/log"
)

func Start() time.Time {
	return time.Now()
}

func logRequest(r *http.Request, status, size int, start time.Time) {
	took := time.Now().Sub(start)
	log.Print("%s %s %s %d %d %s", r.RemoteAddr, r.Method, r.URL, status, size, took)
}

func Error(w http.ResponseWriter, r *http.Request, start time.Time, err error) {
	log.Error("%s", err)
	http.Error(w, fmt.Sprintf("error: %s", err), http.StatusInternalServerError)
	logRequest(r, http.StatusInternalServerError,
		len("error: \n")+len(err.Error()), start)
}

func NotFound(w http.ResponseWriter, r *http.Request, start time.Time) {
	http.Error(w, fmt.Sprintf("not found: %s", r.URL.Path), http.StatusNotFound)
	logRequest(r, http.StatusNotFound,
		len("not found: \n")+len(r.URL.Path), start)
}

func Write(
	w http.ResponseWriter,
	r *http.Request,
	start time.Time,
	message string,
	args ...interface{},
) {
	n, err := fmt.Fprintf(w, message, args...)
	if err != nil {
		log.Error("%s %s: %s", r.Method, r.URL, err)
	} else {
		logRequest(r, http.StatusOK, n, start)
	}
}

func WriteJSON(
	w http.ResponseWriter,
	r *http.Request,
	start time.Time,
	obj interface{},
) {
	blob, err := json.MarshalIndent(obj, "", "  ")
	if err != nil {
		Error(w, r, start, err)
		return
	}
	var n int
	n, err = fmt.Fprintf(w, "%s", blob)
	if err != nil {
		log.Error("%s %s: %s", r.Method, r.URL, err)
	} else {
		logRequest(r, http.StatusOK, n, start)
	}
}

func ServeStatic(dir string) {
	http.Handle("/static/",
		http.StripPrefix("/static/", http.FileServer(http.Dir(dir))))
}
