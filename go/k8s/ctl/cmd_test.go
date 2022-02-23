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
	IsEqual(t, len(cmd.args), 0, "cmd.args")
}

func TestCmdArgs(t *testing.T) {
	cmd := newCmd("testing", "cmd", "args")
	IsEqual(t, cmd.name, "testing", "cmd.name")
	IsEqual(t, len(cmd.args), 2, "cmd.args")
	IsEqual(t, cmd.args[0], "cmd", "cmd.args[0]")
	IsEqual(t, cmd.args[1], "args", "cmd.args[1]")
}
