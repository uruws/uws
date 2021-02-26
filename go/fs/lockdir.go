// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package fs

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"uws/log"
)

var ErrLockDirTimeout error = errors.New("lock dir timeout")

const (
	lockDirWait time.Duration = 500 * time.Millisecond
	lockDirMax  int           = 30 // 15 seconds
)

func lockDirName(name string, checkSource bool) (string, error) {
	fn := filepath.Clean(name)
	if abs, err := filepath.Abs(fn); err != nil {
		return "", err
	} else {
		fn = abs
	}
	if checkSource {
		if st, err := os.Stat(fn); err != nil {
			return "", err
		} else {
			if !st.IsDir() {
				return "", errors.New(fmt.Sprintf("%s: is not a directory", st.Name()))
			}
		}
	}
	fn = fn + ".uwslock"
	return fn, nil
}

func mkLockDir(name string) error {
	fn, err := lockDirName(name, true)
	if err != nil {
		return err
	}
	flag := os.O_CREATE | os.O_EXCL | os.O_TRUNC | os.O_WRONLY
	if fh, err := os.OpenFile(fn, flag, 0600); err != nil {
		return err
	} else {
		defer fh.Close()
		if _, err := fh.WriteString(fmt.Sprintf("%d\n", os.Getpid())); err != nil {
			return err
		}
	}
	return nil
}

func LockDir(name string) error {
	for n := 0; n <= lockDirMax; n += 1 {
		if n == lockDirMax {
			return ErrLockDirTimeout
		}
		if err := mkLockDir(name); err != nil {
			if os.IsExist(err) {
				log.Debug("%s #%d - wait...", err, n)
				time.Sleep(lockDirWait)
			} else {
				return err
			}
		} else {
			return nil
		}
	}
	return nil
}

func UnlockDir(name string) error {
	fn, err := lockDirName(name, false)
	if err != nil {
		return err
	}
	return os.Remove(fn)
}
