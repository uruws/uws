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
	//~ "uws/wapp"
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
	//~ start := wapp.Start()
	ttl, _ := time.ParseDuration(fmt.Sprintf("%ds", c.ttl))
	ctx, cancel := context.WithTimeout(context.Background(), ttl)
	defer cancel()
	cmd := exec.CommandContext(ctx, c.name, c.args...)
	log.Debug("run: %s", cmd)
	//~ if r.URL.Path != "/" {
		//~ wapp.NotFound(w, r, start)
	//~ } else {
		//~ wapp.Write(w, r, start, "index\n")
	//~ }
}
