// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"fmt"
	"net/http"

	"uws/wapp"
)

func NodegroupUpgrade(w http.ResponseWriter, r *http.Request) {
	wapp.Debug(r, "nodegroup upgrade: %s", cluster)
	cmd := fmt.Sprintf("uws%s-nodegroup-upgrade", cluster.Type)
	newCmd(cmd).Run(w, r)
}
