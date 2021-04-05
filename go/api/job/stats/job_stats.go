// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements api job stats manager.
package stats

import (
	"regexp"
	"strings"

	"uws/log"
)

var fieldRe = regexp.MustCompile(`\W`)

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	f = strings.TrimSpace(f)
	return fieldRe.ReplaceAllString(f, "_")
}

type Job struct {
	ID    string
	Name  string
	Label string
	Value int64
}

type Stats struct {
	r map[string]*Job
}

func New() *Stats {
	log.Debug("new")
	return &Stats{}
}

func (s *Stats) List() []*Job {
	l := make([]*Job, 0)
	return l
}

func (s *Stats) Len() int {
	return len(s.r)
}

func (s *Stats) Fetch(dstfn, db_uri string) error {
	log.Debug("fetch")
	log.Debug("dest file %s", dstfn)
	return nil
}

func (s *Stats) Load(fn string) error {
	log.Debug("load file %s", fn)
	return nil
}
