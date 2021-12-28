// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"context"
	"io"
	"io/ioutil"
	"os"
	"os/exec"
	"time"

	"uws/log"
)

var (
	kubeOutFH     func(string, string) (*os.File, error)
	kubeErrFH     func(string, string) (*os.File, error)
	kubeSeekOutFH func(io.Seeker) error
	kubeSeekErrFH func(io.Seeker) error
)

func init() {
	kubeOutFH = ioutil.TempFile
	kubeErrFH = ioutil.TempFile
	kubeSeekOutFH = func(fh io.Seeker) error {
		_, err := fh.Seek(0, 0)
		return err
	}
	kubeSeekErrFH = func(fh io.Seeker) error {
		_, err := fh.Seek(0, 0)
		return err
	}
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
		if err := kubeSeekErrFH(errfh); err != nil {
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
	if err := kubeSeekOutFH(outfh); err != nil {
		return nil, log.DebugError(err)
	}
	return ioutil.ReadAll(outfh)
}
