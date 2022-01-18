// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"

	//~ "uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupK8sCmd string
)

func init() {
	bupK8sCmd = k8sCmd
}

func TestK8sCmd(t *testing.T) {
	IsEqual(t, k8sCmd, "get --raw /metrics", "k8sCmd")
}
