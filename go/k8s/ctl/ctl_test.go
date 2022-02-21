// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"testing"

	. "uws/testing/check"
)

func TestGlobals(t *testing.T) {
	IsEqual(t, kubecmd, "/usr/local/bin/uwskube", "kubecmd")
	IsEqual(t, cluster, "k8stest", "cluster")
}

func TestCluster(t *testing.T) {
	IsEqual(t, Cluster(), "k8stest", "Cluster()")
}
