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
	flag.StringVar(&envFile, "env", "", "load env from yaml `filename`")
	flag.Parse()
	getVar := flag.Arg(0)
	env.Main(envFile, getVar)
}
