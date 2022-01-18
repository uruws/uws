// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"net/http"
	"strings"

	"uws/log"
	"uws/wapp"
)

var k8sCmd string = "get --raw /metrics"

func K8s(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	out, err := Kube(strings.Split(k8sCmd, " ")...)
	if err != nil {
		log.DebugError(err)
		wapp.Error(w, r, start, err)
		return
	}
	// filter the lines we only want, to reduce network usage
	wapp.Write(w, r, start, "%s", out)
}
