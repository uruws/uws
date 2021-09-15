// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package mon implements k8s mon api.
package mon

import (
	"os"
)

var (
	kubecmd string
	cluster string
)

func init() {
	cluster = os.Getenv("UWS_CLUSTER")
	kubecmd = os.Getenv("UWSKUBE")
	if kubecmd == "" {
		kubecmd = "/usr/local/bin/uwskube"
	}
}

func Cluster() string {
	return cluster
}

type statusCondition struct {
	Status string `json:"status"`
	Type   string `json:"type"`
}
