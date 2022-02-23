// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

type ctlCmd struct {
	name string
	args []string
}

func newCmd(name string, args ...string) *ctlCmd {
	return &ctlCmd{
		name: name,
		args: args,
	}
}
