// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"fmt"

	"uws/env"
	"uws/log"
)

func main() {
	log.Init("uwsenv")
	var envName string
	flag.StringVar(&envName, "env", "", "load env `name`")
	flag.Parse()

	if envName != "" {
		if err := env.Load(envName); err != nil {
			log.Fatal("%v", err)
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
