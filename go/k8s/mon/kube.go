// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package mon implements k8s mon api.
package mon

import (
	"context"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"
	"time"

	"uws/k8s/mon/stats"
	"uws/log"
)

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

type cacheEntry struct {
	expire time.Time
	data []byte
}

var cache map[string]*cacheEntry

func init() {
	cache = make(map[string]*cacheEntry)
}

func cacheKey(args ...string) string {
	return stats.CleanFN(strings.Join(args, "_"))
}

func KubeCache(args ...string) ([]byte, error) {
	now := time.Now()
	k := cacheKey(args...)
	e, ok := cache[k]
	if ok {
		if e.expire.Before(now) {
			return e.data, nil
		}
	}
	e = nil
	var err error
	delete(cache, k)
	cache[k] = new(cacheEntry)
	cache[k].data, err = Kube(args...)
	if err != nil {
		return nil, err
	}
	return cache[k].data, nil
}
