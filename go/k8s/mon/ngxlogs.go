// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	"time"

	"uws/log"
	"uws/wapp"
)

type NgxlogsInfo struct {
	Since string `json:"since"`
	Until string `json:"until"`
}

var ngxlogsCmd string = "logs -l app.kubernetes.io/name=proxy --max-log-requests=100 --ignore-errors=true --prefix=true --timestamps=true --limit-bytes=104857600"

func Ngxlogs(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	tl := ngxlogsTimeLimit(time.Now())
	if err := tl.Error(); err != nil {
		wapp.Error(w, r, start, err)
		return
	}
	out, err := Kube(strings.Split(ngxlogsCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	i := new(NgxlogsInfo)
	if err := json.Unmarshal(out, &i); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	//~ i.Since = tl.since
	//~ i.Until = tl.until
	wapp.WriteJSON(w, r, start, &i)
}

type NgxlogsTimeLimit struct {
	err       error
	since     time.Time
	until     time.Time
	unix      int64
	min       int
	min_since int
	min_until int
}

var ngxlogs_time_limit_mock_testing_error bool

func ngxlogsTimeLimit(t time.Time) *NgxlogsTimeLimit {
	if ngxlogs_time_limit_mock_testing_error {
		return &NgxlogsTimeLimit{
			err: errors.New("testing mock error"),
		}
	}
	min := t.Minute()
	min_since := 0
	min_until := 0
	if min >= 55 {
		min_since = 50
		min_until = 55
	} else if min >= 50 {
		min_since = 45
		min_until = 50
	} else if min >= 45 {
		min_since = 40
		min_until = 45
	} else if min >= 40 {
		min_since = 35
		min_until = 40
	} else if min >= 35 {
		min_since = 30
		min_until = 35
	} else if min >= 30 {
		min_since = 25
		min_until = 30
	} else if min >= 25 {
		min_since = 20
		min_until = 25
	} else if min >= 20 {
		min_since = 15
		min_until = 20
	} else if min >= 15 {
		min_since = 10
		min_until = 15
	} else if min >= 10 {
		min_since = 5
		min_until = 10
	} else if min >= 5 {
		min_since = 0
		min_until = 5
	} else if min >= 0 {
		min_since = 55
		min_until = 0
	}
	// quite basic way to do it, but it works!
	return &NgxlogsTimeLimit{
		unix:      t.Unix(),
		min:       min,
		min_since: min_since,
		min_until: min_until,
	}
}

func (t *NgxlogsTimeLimit) Error() error {
	return t.err
}
