// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements ngxlogs cmd.
package main

import (
	"uws/log"
)

func main() {
	log.Init("ngxlogs")
	log.Debug("start...")
	log.Debug("end...")
}
