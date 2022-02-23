// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"testing"

	. "uws/testing/check"
)

func TestCmd(t *testing.T) {
	cmd := newCmd("testing")
	IsEqual(t, cmd.name, "testing", "cmd.name")
}
