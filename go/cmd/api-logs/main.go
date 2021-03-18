// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-logs cmd.
package main

import (
	"flag"
	"path/filepath"
)

func main() {
	var (
		statedir string = filepath.FromSlash("/uws/var/api/logs")
	)
	flag.StringVar(&statedir, "statedir", statedir, "directory where to keep state info")
	flag.Parse()
}
