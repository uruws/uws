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

func LogError(r *http.Request, format string, v ...interface{}) {
	msg := fmt.Sprintf(format, v...)
	log.Error("%s %s %s: %s", r.RemoteAddr, r.Method, r.URL, msg)
}

func Debug(r *http.Request, format string, v ...interface{}) {
	msg := fmt.Sprintf(format, v...)
	log.Debug("%s %s %s: %s", r.RemoteAddr, r.Method, r.URL, msg)
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

func BadRequest(w http.ResponseWriter, r *http.Request, start time.Time) {
	st := http.StatusBadRequest
	msg := fmt.Sprintf("bad request: %s", r.URL.Path)
	http.Error(w, msg, st)
	logRequest(r, st, len("\n")+len(msg), start)
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

func WriteJSONStatus(
	w http.ResponseWriter,
	r *http.Request,
	start time.Time,
	status int,
	obj interface{},
) {
	blob, err := json.Marshal(obj)
	if err != nil {
		Error(w, r, start, err)
		return
	}
	w.Header().Set("content-type", "application/json")
	w.WriteHeader(status)
	var n int
	n, err = fmt.Fprintf(w, "%s", blob)
	if err != nil {
		log.Error("%s %s: %s", r.Method, r.URL, err)
	} else {
		logRequest(r, status, n, start)
	}
}

func WriteJSON(
	w http.ResponseWriter,
	r *http.Request,
	start time.Time,
	obj interface{},
) {
	WriteJSONStatus(w, r, start, http.StatusOK, obj)
}

func ServeStatic(dir string) {
	http.Handle("/static/",
		http.StripPrefix("/static/", http.FileServer(http.Dir(dir))))
}
