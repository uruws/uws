// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"fmt"

	"uws/env"
)

func main() {
	flag.Parse()
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
