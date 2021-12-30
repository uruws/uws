// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"
	"strings"

	"uws/log"
	"uws/wapp"
)

type topNodes struct {
	Count uint   `json:"count"`
	Sum   uint64 `json:"sum"`
}

var topNodesCmd string = "top nodes --no-headers"

func parseTopNodes(tn *topNodes, out []byte) error {
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			tn.Count++
		}
	}
	return nil
}

func TopNodes(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(topNodesCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	tn := new(topNodes)
	if err := parseTopNodes(tn, out); err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	wapp.WriteJSON(w, r, start, &tn)
}
