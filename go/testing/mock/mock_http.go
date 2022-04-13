// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mock

import (
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"net/url"
	"strings"
)

func HTTPListenAndServe(addr string, h http.Handler) error {
	return nil
}

func HTTPRequest() *http.Request {
	return httptest.NewRequest("GET", "/", nil)
}

func HTTPRequestPost(query string) *http.Request {
	if query == "" {
		return httptest.NewRequest("POST", "/", nil)
	}
	v, err := url.ParseQuery(query)
	if err != nil {
		panic(err)
	}
	body := strings.NewReader(v.Encode())
	r := httptest.NewRequest("POST", "/", body)
	r.Header.Set("content-type", "application/x-www-form-urlencoded")
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
