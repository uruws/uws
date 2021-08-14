// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package mon implements k8s mon api.
package mon

import (
	"context"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"regexp"
	"strings"
	"time"

	"uws/log"
)

var (
	kubecmd string
	cluster string
)

func init() {
	cluster = os.Getenv("UWS_CLUSTER")
	kubecmd = os.Getenv("UWSKUBE")
	if kubecmd == "" {
		kubecmd = "/usr/local/bin/uwskube"
	}
}

func Cluster() string {
	return cluster
}

var fnre = regexp.MustCompile(`\W`)

func CleanFN(n string) string {
	fn := strings.TrimSpace(n)
	return fnre.ReplaceAllString(fn, "_")
}

type Buffer struct {
	buf *strings.Builder
}

func NewBuffer() *Buffer {
	return &Buffer{buf: new(strings.Builder)}
}

func (b *Buffer) String() string {
	return b.buf.String()
}

func (b *Buffer) Write(format string, args ...interface{}) error {
	_, err := b.buf.WriteString(fmt.Sprintf(format, args...))
	if err != nil {
		log.Error("%s", err)
	}
	return err
}

func Kube(args ...string) ([]byte, error) {
	var (
		outfh *os.File
		errfh *os.File
		err   error
	)
	outfh, err = ioutil.TempFile("", "kube-out.*")
	if err != nil {
		return nil, log.DebugError(err)
	}
	defer func() {
		os.Remove(outfh.Name())
		outfh.Close()
	}()
	errfh, err = ioutil.TempFile("", "kube-err.*")
	if err != nil {
		return nil, log.DebugError(err)
	}
	defer func() {
		os.Remove(errfh.Name())
		errfh.Close()
	}()
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Minute)
	defer cancel()
	cmd := exec.CommandContext(ctx, kubecmd, args...)
	cmd.Stdout = outfh
	cmd.Stderr = errfh
	log.Debug("run: %s", cmd)
	xerr := cmd.Run()
	if xerr != nil {
		if _, err := errfh.Seek(0, 0); err != nil {
			log.Error("errfh seek: %s", err)
		} else {
			if blob, err := ioutil.ReadAll(errfh); err != nil {
				log.Error("errfh read: %s", err)
			} else {
				if len(blob) > 0 {
					log.Error("%s", blob)
				}
			}
		}
		return nil, log.DebugError(xerr)
	}
	if _, err := outfh.Seek(0, 0); err != nil {
		return nil, log.DebugError(err)
	}
	return ioutil.ReadAll(outfh)
}
