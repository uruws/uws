// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

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

type ctlCmd struct {
	name   string
	args   []string
	bindir string
	ttl    int
}

func newCmd(name string, args ...string) *ctlCmd {
	return &ctlCmd{
		name:   name,
		args:   args,
		bindir: bindir,
		ttl:    300, // 5min
	}
}

func (c *ctlCmd) Run(r *http.Request) {
	//~ start := wapp.Start()
	ttl, _ := time.ParseDuration(fmt.Sprintf("%ds", c.ttl))
	ctx, cancel := context.WithTimeout(context.Background(), ttl)
	defer cancel()
	cmdpath := filepath.Clean(filepath.Join(c.bindir, c.name))
	cmd := exec.CommandContext(ctx, cmdpath, c.args...)
	wapp.Debug(r, "run: %s", cmd)
	out, err := cmd.CombinedOutput()
	if err != nil {
		wapp.LogError(r, "%s: %s", cmd, err)
		wapp.Debug(r, "%s", out)
		//~ code := -128
		//~ switch err.(type) {
		//~ case *exec.ExitError:
			//~ p := err.(*exec.ExitError).ProcessState
			//~ code = p.ExitCode()
		//~ }
		//~ st := newStatus(code, string(out))
		//~ st.Error = err.Error()
		//~ wapp.WriteJSONStatus(w, r, start, http.StatusInternalServerError, st)
	} else {
		//~ st := newStatus(0, string(out))
		//~ wapp.WriteJSON(w, r, start, st)
	}
}

func ExecHandler(w http.ResponseWriter, r *http.Request) {
	wapp.Debug(r, "exec handler: %s", cluster)
	start := wapp.Start()
	if r.Method == "POST" {
		cmd := r.PostFormValue("cmd")
		if cmd == "" {
			wapp.Error(w, r, start, errors.New("no command"))
		} else {
			args := r.PostForm["args"]
			wapp.Debug(r, "exec: %s %v", cmd, args)
			go doExec(r, cmd, args...)
			wapp.Write(w, r, start, "dispatch ok\n")
		}
	} else {
		wapp.LogError(r, "invalid method: %s", r.Method)
		wapp.BadRequest(w, r, start)
	}
}

func doExec(r *http.Request, cmd string, args ...string) {
	wapp.Debug(r, "do exec: %s %v", cmd, args)
	newCmd(cmd, args...).Run(r)
}

func cmdRun(w http.ResponseWriter, r *http.Request, cmd string, args ...string) {
	wapp.Debug(r, "%s %v", cmd, args)
}
