// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"fmt"
	"net/http"

	"uws/log"
)

func NodegroupUpgrade(w http.ResponseWriter, r *http.Request) {
	log.Debug("nodegroup upgrade: %s (%s)", cluster, cluster.Type)
	cmd := fmt.Sprintf("uws%s-nodegroup-upgrade", cluster.Type)
	newCmd(cmd).Run(w, r)
}
