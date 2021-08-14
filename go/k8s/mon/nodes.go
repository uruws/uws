// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"

	"uws/wapp"
)

func NodesConfig(w http.ResponseWriter, r *http.Request) {
	wapp.Write(w, r, "nodes config\n")
}

func Nodes(w http.ResponseWriter, r *http.Request) {
	wapp.Write(w, r, "nodes\n")
}
