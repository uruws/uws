// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"time"

	"uws/log"
)

var userAgent string = "uwsbot/" + version
const reqTTL time.Duration = 5 * time.Minute

func newRequest(script, method, uri string) (*http.Request, error) {
	r, err := http.NewRequest(method, uri, nil)
	r.Header.Set("user-agent", userAgent)
	r.Header.Set("x-uwsbot", fmt.Sprintf("%s-%d", script, time.Now().UnixNano()))
	return r, err
}

func newPostFormRequest(script, uri string, v url.Values) *http.Request {
	r, err := newRequest(script, "POST", uri)
	if err != nil {
		log.Fatal("bot new post form request: %s", err)
	}
	r.Header.Set("content-type", "application/x-www-form-urlencoded")
	if len(v) > 0 {
		fh, err := ioutil.TempFile("", "uwsbot_post_*.form")
		if err != nil {
			log.Fatal("bot new post form values: %s", err)
		}
		if _, err := fh.WriteString(v.Encode()); err != nil {
			log.Fatal("bot new post body: %s", err)
		}
		if err := os.Remove(fh.Name()); err != nil {
			log.Error("bot new post could not remove tempfile: %s", err)
		}
		if _, err := fh.Seek(0, 0); err != nil {
			log.Fatal("bot new post body: %s", err)
		}
		r.Body = fh
	}
	return r
}

func newGetRequest(script, uri string) *http.Request {
	r, err := newRequest(script, "GET", uri)
	if err != nil {
		log.Fatal("bot new get request: %s", err)
	}
	return r
}

func requestAuth(req *http.Request, authToken, userId string) {
	req.Header.Set("x-auth-token", authToken)
	req.Header.Set("x-user-id", userId)
}
