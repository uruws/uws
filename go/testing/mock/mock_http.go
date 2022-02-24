// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mock

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"strings"
)

func HTTPListenAndServe(addr string, h http.Handler) error {
	return nil
}

func HTTPRequest() *http.Request {
	r := httptest.NewRequest("GET", "/", nil)
	return r
}

func HTTPResponse() *httptest.ResponseRecorder {
	return httptest.NewRecorder()
}

func HTTPResponseString(resp *http.Response) string {
	defer resp.Body.Close()
	blob, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err.Error()
	}
	return strings.TrimSpace(string(blob))
}
