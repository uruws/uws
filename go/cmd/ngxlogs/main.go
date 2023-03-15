// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements ngxlogs cmd.
package main

import (
	"flag"

	"uws/log"
	"uws/ngxlogs"
)

func main() {
	f := ngxlogs.NewFlags()

	flag.BoolVar(&f.Errors, "error", false, "show errors only")
	flag.StringVar(&f.Input, "input", "-", "read from file")
	flag.BoolVar(&f.Raw, "raw", false, "show raw input")

	flag.Parse()

	log.Init("ngxlogs")
	log.NoDateTime()
	log.Debug("start...")

	ngxlogs.Main(f)

	log.Debug("end...")
}
