// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	//~ "uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupTopNodesCmd string
)

func init() {
	bupTopNodesCmd = topNodesCmd
}

func TestTopNodesCmd(t *testing.T) {
	IsEqual(t, topNodesCmd, "top nodes --no-headers", "top nodes cmd")
}
