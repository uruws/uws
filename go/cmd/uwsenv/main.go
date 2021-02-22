// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"

	"uws/env"
)

func main() {
	var envFile string
	flag.StringVar(&envFile, "env", "", "load env file")
	flag.Parse()
	env.Main(envFile)
}
