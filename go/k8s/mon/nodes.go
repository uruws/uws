// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"

	"uws/wapp"
)

func NodesConfig(w http.ResponseWriter, r *http.Request) {
	out, err := Kube("get", "nodes", "-o", "json")
	if err != nil {
		wapp.Error(w, r, err)
	} else {
		wapp.Write(w, r, "%s", out)
	}
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	wapp.Write(w, r, "nodes\n")
}
