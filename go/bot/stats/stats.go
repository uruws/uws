// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements bot stats generator/manager.
package stats

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"uws/env"
	"uws/fs"
	"uws/log"
)

var (
	fieldRe  *regexp.Regexp
)

func init() {
	// regexp: \W not word characters (== [^0-9A-Za-z_])
	fieldRe = regexp.MustCompile(`\W`)
}

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	return fieldRe.ReplaceAllString(f, "_")
}

type Stats struct {
	stdir  string
	fname  string
	tmpdir string
}

func New(fieldName ...string) *Stats {
	stdir := env.GetFilepath("STATSDIR")
	fname := cleanFieldName(fieldName...)
	tmpdir, err := ioutil.TempDir("", "uwsbot-stats-*")
	if err != nil {
		log.Fatal("stats new: %s", err)
	}
	log.Debug("new %s %s %s", stdir, fname, tmpdir)
	return &Stats{stdir, fname, tmpdir}
}

func Save(st *Stats) {
	dst := filepath.Join(st.stdir, st.fname)
	log.Debug("stats lock %s", dst)
	if err := fs.LockDir(dst); err != nil {
		log.Fatal("stats lock: %s", err)
	}
	defer fs.UnlockDir(dst)
	log.Debug("stats save remove %s", dst)
	os.RemoveAll(dst)
	log.Debug("stats save: %s -> %s", st.tmpdir, dst)
	if err := os.MkdirAll(st.stdir, 0750); err != nil {
		log.Fatal("stats save: %s", err)
	}
	if err := os.Rename(st.tmpdir, dst); err != nil {
		log.Fatal("stats save: %s", err)
	}
}
