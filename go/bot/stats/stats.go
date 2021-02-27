// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements bot stats generator/manager.
package stats

import (
	"encoding/json"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

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
	start  time.Time
	child  bool
	benv   string
	bname  string
}

func newStats(fieldName ...string) *Stats {
	stdir := env.GetFilepath("STATSDIR")
	fname := cleanFieldName(fieldName...)
	return &Stats{stdir: stdir, fname: fname, start: time.Now(), child: false}
}

func New(fieldName ...string) *Stats {
	var err error
	st := newStats(fieldName...)
	st.tmpdir, err = ioutil.TempDir("", "uwsbot-stats-*")
	if err != nil {
		log.Fatal("stats new: %s", err)
	}
	log.Debug("new %s %s %s", st.stdir, st.fname, st.tmpdir)
	return st
}

func NewChild(benv, bname, tmpdir string, fieldName ...string) *Stats {
	st := newStats(fieldName...)
	st.child = true
	st.benv = benv
	st.bname = bname
	st.tmpdir = tmpdir
	log.Debug("new child %s %s %s", st.stdir, st.fname, st.tmpdir)
	return st
}

func (s *Stats) Dirname() string {
	return s.tmpdir
}

func Save(st *Stats) {
	saveStats(st)
	if st.child {
		return
	}
	dst := filepath.Join(st.stdir, st.fname)
	if err := os.MkdirAll(dst, 0750); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats save: %s", err)
	}
	log.Debug("stats lock %s", dst)
	if err := fs.LockDir(dst); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats lock: %s", err)
	}
	defer fs.UnlockDir(dst)
	log.Debug("stats save remove %s", dst)
	os.RemoveAll(dst)
	log.Debug("stats save: %s -> %s", st.tmpdir, dst)
	if err := os.Rename(st.tmpdir, dst); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats save: %s", err)
	}
}

type StatsInfo struct {
	Id string `json:"id"`
	Label string `json:"label"`
	Value int64 `json:"value"`
}

func saveStats(st *Stats) {
	var fn string
	if st.child {
		fn = filepath.Join(st.tmpdir, st.fname + ".stats")
	} else {
		fn = filepath.Join(st.tmpdir, "stats")
	}
	log.Debug("save (child:%v) stats %s", st.child, fn)
	inf := &StatsInfo{
		Id: st.fname,
		Label: st.fname,
		Value: time.Now().Sub(st.start).Milliseconds(),
	}
	blob, err := json.Marshal(inf)
	if err != nil {
		log.Fatal("save stats %s: %s", fn, err)
	}
	if err := ioutil.WriteFile(fn, blob, 0640); err != nil {
		log.Fatal("save stats: %s", err)
	}
}
