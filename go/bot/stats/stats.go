// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements bot stats generator/manager.
package stats

import (
	"regexp"
	"strings"

	"uws/env"
	"uws/log"
)

var (
	statsDir string
	fieldRe  *regexp.Regexp
)

func init() {
	statsDir = env.GetFilepath("STATSDIR")
	// regexp: \W not word characters (== [^0-9A-Za-z_])
	fieldRe = regexp.MustCompile(`\W`)
}

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	return fieldRe.ReplaceAllString(f, "_")
}

func Init(benv, bname string) {
	f := cleanFieldName(benv, bname)
	log.Debug("init %s %s: %s", benv, bname, f)
}
