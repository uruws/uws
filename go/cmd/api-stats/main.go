// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-stats cmd.
package main

import (
	"flag"
	//~ "io/ioutil"
	//~ "os"
	"path/filepath"
	//~ "strings"

	//~ "uws/api/stats"
	"uws/log"
)

func main() {
	log.Init("api-stats")
	var (
		statsdir string = filepath.FromSlash("/uws/var/api/stats")
		env      string = "default"
	)
	flag.StringVar(&statsdir, "statsdir", statsdir,
		"directory `where` to load stats info from")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.Parse()
}
