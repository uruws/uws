// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"context"
	"fmt"
	"net/http"
	"os/exec"
	"time"

	"uws/log"
	"uws/wapp"
)

type ctlCmd struct {
	name string
	args []string
	bindir string
	ttl int
}

func newCmd(name string, args ...string) *ctlCmd {
	return &ctlCmd{
		name: name,
		args: args,
		bindir: bindir,
		ttl: 300, // 5min
	}
}

func (c *ctlCmd) Run(w http.ResponseWriter, r *http.Request) {
	start := wapp.Start()
	ttl, _ := time.ParseDuration(fmt.Sprintf("%ds", c.ttl))
	ctx, cancel := context.WithTimeout(context.Background(), ttl)
	defer cancel()
	cmd := exec.CommandContext(ctx, c.name, c.args...)
	log.Debug("run: %s", cmd)
	out, err := cmd.CombinedOutput()
	if err != nil {
		log.Error("%s: %s", cmd, err)
		log.Debug("%s", out)
		code := -128
		switch err.(type) {
		case *exec.ExitError:
			p := err.(*exec.ExitError).ProcessState
			code = p.ExitCode()
		}
		st := newStatus(code, string(out))
		wapp.WriteJSONStatus(w, r, start, http.StatusInternalServerError, st)
	} else {
		st := newStatus(0, string(out))
		wapp.WriteJSON(w, r, start, st)
	}
}
