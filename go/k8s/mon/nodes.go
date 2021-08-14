// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"

	"uws/wapp"
)

func NodesConfig(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		wapp.Error(w, r, start, err)
	} else {
		wapp.Write(w, r, start, "%s", out)
	}
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	wapp.Write(w, r, start, "nodes\n")
}
