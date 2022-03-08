// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/url"
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

func (c *ctlCmd) String() string {
	return filepath.Join(c.bindir, c.name)
}

func (c *ctlCmd) Run(r *http.Request) (string, error) {
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
		return "", err
	}
	return string(out), nil
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
	x := newCmd(cmd, args...)
	outs, err := x.Run(r)
	sendmail(r, x.String(), outs, err)
}

func sendmail(r *http.Request, origcmd, out string, err error) {
	wapp.Debug(r, "sendmail: origcmd='%s' error='%v'", origcmd, err)
	subject := fmt.Sprintf("[OK] %s", origcmd)
	mailto := "root@localhost"
	msg := out
	if err != nil {
		subject = fmt.Sprintf("[FAIL] %s", origcmd)
		mailto = "munin-alert@localhost"
		msg = fmt.Sprintf("ERROR: %s\n\n%s", err.Error(), out)
	}
	args := []string{
		"-s",
		subject,
		"--",
		mailto,
	}
	ctx, cancel := context.WithTimeout(context.Background(), 60)
	defer cancel()
	cmd := exec.CommandContext(ctx, mailx, args...)
	wapp.Debug(r, "sendmail: %s", cmd)
	stdin, xerr := cmd.StdinPipe()
	if xerr != nil {
		wapp.LogError(r, "sendmail: %s", xerr)
		return
	}
	defer stdin.Close()
	xerr = cmd.Start()
	if xerr != nil {
		wapp.LogError(r, "sendmail: %s", xerr)
		return
	}
	_, xerr = fmt.Fprint(stdin, msg)
	if xerr != nil {
		wapp.LogError(r, "sendmail: %s", xerr)
	}
	xerr = cmd.Wait()
	if xerr != nil {
		wapp.LogError(r, "sendmail: %s", xerr)
	}
}

func cmdRun(w http.ResponseWriter, r *http.Request, cmd string, args ...string) {
	wapp.Debug(r, "%s %v", cmd, args)
	start := wapp.Start()
	resp, err := http.PostForm(execurl,
		url.Values{"cmd": {cmd}, "args": args})
	if err != nil {
		wapp.Error(w, r, start, err)
		return
	}
	if resp.StatusCode != http.StatusOK {
		wapp.Error(w, r, start, errors.New(resp.Status))
		return
	}
	wapp.Write(w, r, start, "ok")
}
