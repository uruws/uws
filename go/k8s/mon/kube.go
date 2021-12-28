// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"context"
	"io/ioutil"
	"os"
	"os/exec"
	"time"

	"uws/log"
)

var (
	kubeOutFH func(string, string) (*os.File, error)
	kubeErrFH func(string, string) (*os.File, error)
)

func init() {
	kubeOutFH = ioutil.TempFile
	kubeErrFH = ioutil.TempFile
}

func Kube(args ...string) ([]byte, error) {
	var (
		outfh *os.File
		errfh *os.File
		err   error
	)
	outfh, err = kubeOutFH("", "kube-out.*")
	if err != nil {
		return nil, log.DebugError(err)
	}
	defer func() {
		os.Remove(outfh.Name())
		outfh.Close()
	}()
	errfh, err = kubeErrFH("", "kube-err.*")
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
		return nil, xerr
	}
	if _, err := outfh.Seek(0, 0); err != nil {
		return nil, log.DebugError(err)
	}
	return ioutil.ReadAll(outfh)
}
