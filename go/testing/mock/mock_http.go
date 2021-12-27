// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mock

import (
	"net/http"
	"net/http/httptest"
)

func HTTPListenAndServe(addr string, h http.Handler) error {
	return nil
}

func HTTPRequest(method, target string) *http.Request {
	return httptest.NewRequest(method, target, nil)
}

func HTTPResponse() *httptest.ResponseRecorder {
	return httptest.NewRecorder()
}
