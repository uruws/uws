// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package api

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"os/exec"
	"path/filepath"
	"time"

	"uws/wapp"
)

type apiCmd struct {
	name   string
	args   []string
	bindir string
	ttl    int
}

func newCmd(name string, args ...string) *apiCmd {
	return &apiCmd{
		name:   name,
		args:   args,
		bindir: bindir,
		ttl:    cmdttl,
	}
}

func (c *apiCmd) String() string {
	return filepath.Clean(filepath.Join(c.bindir, c.name))
}

func (c *apiCmd) Run(r *http.Request) (string, error) {
	ttl, _ := time.ParseDuration(fmt.Sprintf("%ds", c.ttl))
	ctx, cancel := context.WithTimeout(context.Background(), ttl)
	defer cancel()
	cmd := exec.CommandContext(ctx, c.String(), c.args...)
	wapp.Debug(r, "run: %s", cmd)
	out, err := cmd.CombinedOutput()
	if err != nil {
		wapp.LogError(r, "%s: %s", cmd, err)
		wapp.Debug(r, "%s", out)
		return string(out), err
	}
	return string(out), nil
}

func ExecHandler(w http.ResponseWriter, r *http.Request) {
	wapp.Debug(r, "exec handler")
	start := wapp.Start()
	if r.Method == "POST" {
		cmd := r.PostFormValue("cmd")
		if cmd == "" {
			wapp.Error(w, r, start, errors.New("no command"))
		} else {
			args := r.PostForm["args"]
			doExec(w, r, start, cmd, args...)
		}
	} else {
		wapp.LogError(r, "invalid method: %s", r.Method)
		wapp.BadRequest(w, r, start)
	}
}

func newApiCmd(name string, args ...string) *apiCmd {
	xargs := make([]string, 0)
	xargs = append(xargs, name)
	for _, a := range args {
		xargs = append(xargs, a)
	}
	return newCmd("uwsapi-ssh.sh", xargs...)
}

func doExec(w http.ResponseWriter, r *http.Request, start time.Time, cmd string, args ...string) {
	wapp.Debug(r, "exec: %s %v", cmd, args)
	x := newApiCmd(cmd, args...)
	outs, err := x.Run(r)
	if err != nil {
		wapp.LogError(r, "%s", err)
		wapp.Error(w, r, start, errors.New("internal exec call"))
		return
	}
	wapp.Write(w, r, start, outs)
}
