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

type topNodes struct {
}

var topNodesCmd string = "top nodes --no-headers"

func TopNodes(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(topNodesCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	tn := new(topNodes)
	if err := json.Unmarshal(out, &tn); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	wapp.WriteJSON(w, r, start, &tn)
}
