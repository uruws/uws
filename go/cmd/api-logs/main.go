// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-logs cmd.
package main

import (
	"flag"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"

	"uws/log"
)

func main() {
	log.Init("api-logs")
	var (
		statedir string = filepath.FromSlash("/uws/var/api/logs")
		logsdir  string = filepath.FromSlash("/uws/var/api/logs")
		env      string = "default"
		filter   string = "heroku.log"
	)
	flag.StringVar(&statedir, "statedir", statedir, "directory `where` to keep state info")
	flag.StringVar(&logsdir, "logsdir", logsdir, "directory `where` to read logs from")
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
		last, err = Filter(last, filter, logsdir, env)
	}
	if err != nil {
		log.Fatal("%s", err)
	}
	if err := ioutil.WriteFile(lastfn, []byte(last), 0660); err != nil {
		log.Fatal("%s", err)
	}
}

// Filter parses log lines from filename (stdin if - provided) and avoid duplicates from previous runs.
func Filter(last, filename, logsdir, env string) (string, error) {
	var fh *os.File
	if filename == "-" {
		return scan(last, os.Stdin)
	} else {
		var err error
		fn := filepath.Join(filepath.Clean(logsdir),
			filepath.Clean(env), filepath.Clean(filename))
		fh, err = os.Open(fn)
		if err != nil {
			return "", err
		}
		defer fh.Close()
		return scan(last, fh)
	}
}

func scan(last string, fh io.Reader) (string, error) {
	log.Debug("scan last '%s'", last)
	new := ""
	return new, nil
}
