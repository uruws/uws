// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"net/http"

	"uws/log"
)

func NodegroupUpgrade(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodegroup upgrade: %s", cluster)
	newCmd("false").Run(w, r)
}
