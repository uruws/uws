// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package main

import (
	"errors"
	"net/http"

	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupListenAndServe func(string, http.Handler) error
	bupOsHostname     func() (string, error)
)

func init() {
	bupListenAndServe = listenAndServe
	bupOsHostname = osHostname
}

func mockOsHostnameError() {
	osHostname = func() (string, error) {
		return "", errors.New("mock_error")
	}
}

func mockOsHostnameReset() {
	osHostname = nil
	osHostname = bupOsHostname
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

func TestHealthzHandlerError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	mockOsHostnameError()
	defer mockOsHostnameReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	healthzHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "error: mock_error", "resp body")
}

func TestPingHandler(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	pingHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	h, _ := osHostname()
	IsEqual(t, mock.HTTPResponseString(resp), "ctl@"+h, "resp body")
}

func TestPingHandlerError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	mockOsHostnameError()
	defer mockOsHostnameReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	pingHandler(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp), "error: mock_error", "resp body")
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
