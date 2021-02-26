// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"
	"time"

	"uws/log"
)

const reqTTL time.Duration = 5 * time.Minute

func newRequest(method, uri string) (*http.Request, error) {
	return http.NewRequest(method, uri, nil)
}

func newPostFormRequest(uri string) *http.Request {
	r, err := newRequest("POST", uri)
	if err != nil {
		log.Fatal("bot new post form request: %s", err)
	}
	r.Header.Set("content-type", "application/x-www-form-urlencoded")
	return r
}

func requestAuth(req *http.Request, authToken, userId string) {
	req.Header.Set("x-auth-token", authToken)
	req.Header.Set("x-user-id", userId)
}
