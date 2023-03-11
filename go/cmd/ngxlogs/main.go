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

	flag.StringVar(&f.Input, "input", "-", "read from file")
	flag.StringVar(&f.Format, "format", "json", "input file format")

	flag.Parse()

	log.Init("ngxlogs")
	log.NoDateTime()
	log.Debug("start...")

	ngxlogs.Main(f)

	log.Debug("end...")
}
