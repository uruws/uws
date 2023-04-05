// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"encoding/json"
	"net/http"
	"strings"

	"uws/log"
	"uws/wapp"
)

type NgxlogsInfo struct {
	Since string `json:"since"`
}

var ngxlogsCmd string = "logs -l 'app.kubernetes.io/name=proxy --max-log-requests 100 --ignore-errors=true --prefix=true --timestamps=true"

func Ngxlogs(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	since := ngxlogsSince()
	if since == "" {
		err := log.Error("%s", "could not get ngxlogs since time value")
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
	i.Since = since
	wapp.WriteJSON(w, r, start, &i)
}

func ngxlogsSince() string {
	return "FIXME"
}
