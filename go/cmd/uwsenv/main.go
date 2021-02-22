// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"fmt"
	"log"

	"uws/env"
)

func main() {
	var envFile string
	flag.StringVar(&envFile, "env", "", "load env from yaml `filename`")
	flag.Parse()
	getVar := flag.Arg(0)
	if envFile != "." {
		if err := env.Load(envFile); err != nil {
			log.Fatal(err)
		}
	}
	if getVar != "" {
		fmt.Printf("%s\n", env.Get(getVar))
	} else {
		for _, k := range env.List() {
			fmt.Printf("%s=\"%s\"\n", k, env.Get(k))
		}
	}
}
