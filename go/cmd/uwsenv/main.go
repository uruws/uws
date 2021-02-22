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
	if envFile != "." {
		if err := env.Load(envFile); err != nil {
			log.Fatal(err)
		}
	}
	if flag.NArg() > 0 {
		for _, getVar := range flag.Args() {
			fmt.Printf("%s\n", env.Get(getVar))
		}
	} else {
		for _, k := range env.List() {
			fmt.Printf("%s=\"%s\"\n", k, env.Get(k))
		}
	}
}
