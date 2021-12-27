// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package main

import (
	"net/http"

	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupListenAndServe func(string, http.Handler) error
)

func init() {
	bupListenAndServe = listenAndServe
}

func TestMainPanics(t *testing.T) {
	out := mock.Logger()
	defer mock.LoggerReset()
	cluster = ""
	defer func() {
		cluster = "k8stest"
	}()
	Panics(t, main, "main")
	Match(t, "\\[FATAL\\] UWS_CLUSTER not set", out.String(), "error log")
}

func TestMain(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	listenAndServe = mock.HTTPListenAndServe
	defer func() {
		listenAndServe = bupListenAndServe
	}()
	Panics(t, main, "main")
}

func TestMainHandler(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	r.URL.Path = "/"
	mainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "index", "resp body")
}

func TestMainHandlerNotFound(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	mainHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 404, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "not found: /testing", "resp body")
}

func TestHealthzHandler(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	healthzHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "ok", "resp body")
}

func TestPingHandler(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	pingHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "uwsctl@go-devel.uws.local", "resp body")
}
