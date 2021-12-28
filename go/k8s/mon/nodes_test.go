// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	//~ "uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupNodesCmd string
)

func init() {
	bupNodesCmd = nodesCmd
}

func TestNodesCmd(t *testing.T) {
	IsEqual(t, nodesCmd, "get nodes -o json", "nodes cmd")
}
