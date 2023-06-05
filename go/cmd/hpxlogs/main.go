// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements hpxlogs cmd, an internal haproxy logs parser.
package main

import (
	"flag"

	"uws/hpxlogs"
	"uws/log"
)

func main() {
	var (
		noStats bool
	)

	f := hpxlogs.NewFlags()

	flag.BoolVar(&f.Errors, "error", false, "show errors only")
	flag.StringVar(&f.Input, "input", "-", "read from file")
	flag.BoolVar(&f.Raw, "raw", false, "show raw input")
	flag.BoolVar(&noStats, "no-stats", false, "disable stats information")
	flag.BoolVar(&f.Quiet, "quiet", false, "reduce verbosity")

	flag.Parse()

	if noStats {
		f.Stats = false
	}

	log.Init("hpxlogs")
	log.NoDateTime()
	log.Debug("start...")

	hpxlogs.Main(f)

	log.Debug("end...")
}
