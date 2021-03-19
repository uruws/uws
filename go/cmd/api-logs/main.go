// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-logs cmd.
package main

import (
	"flag"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"

	"uws/api/stats"
	"uws/fs"
	"uws/log"
)

func main() {
	log.Init("api-logs")
	var (
		statedir string = filepath.FromSlash("/uws/var/api/logs")
		logsdir  string = filepath.FromSlash("/uws/var/api/logs")
		statsdir string = filepath.FromSlash("/uws/var/api/stats")
		env      string = "default"
		filter   string = ""
	)
	flag.StringVar(&statedir, "statedir", statedir, "directory `where` to keep state info")
	flag.StringVar(&logsdir, "logsdir", logsdir, "directory `where` to read logs from")
	flag.StringVar(&statsdir, "statsdir", statsdir, "directory `where` to keep stats info")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.StringVar(&filter, "filter", filter, "filter log `file`")
	flag.Parse()

	lastfn := filepath.Join(filepath.Clean(statedir), filepath.Clean(env), ".api-logs.last")
	last := ""
	if blob, err := ioutil.ReadFile(lastfn); err != nil {
		log.Debug("read lastfn: %s", err)
	} else {
		last = strings.TrimSpace(string(blob))
	}

	var err error
	if filter != "" {
		last, err = Filter(last, filter, logsdir, statsdir, env)
	}
	if err != nil {
		log.Fatal("%s", err)
	}
	if err := ioutil.WriteFile(lastfn, []byte(last), 0640); err != nil {
		log.Fatal("%s", err)
	}
}

// Filter parses log lines from filename (stdin if - provided) and avoid duplicates from previous runs.
func Filter(last, filename, logsdir, statsdir, env string) (string, error) {
	var fh *os.File
	var err error
	st := stats.NewReg()
	if filename == "-" {
		last, err = stats.Scan(st, last, os.Stdin)
	} else {
		fn := filepath.Join(filepath.Clean(logsdir),
			filepath.Clean(env), filepath.Clean(filename))
		fh, err = os.Open(fn)
		if err != nil {
			return "", err
		}
		defer fh.Close()
		last, err = stats.Scan(st, last, fh)
	}
	if err != nil {
		return "", err
	}
	if st.Len() > 0 {
		log.Debug("stats %d", st.Len())
		fn := filepath.Join(filepath.Clean(statsdir),
			filepath.Clean(env), "stats.json")
		lockd := filepath.Dir(fn)
		fs.LockDir(lockd)
		defer fs.UnlockDir(lockd)
		if err := ioutil.WriteFile(fn, st.Encode(), 0664); err != nil {
			return "", err
		}
		log.Debug("%s: saved!", fn)
	}
	return last, err
}
