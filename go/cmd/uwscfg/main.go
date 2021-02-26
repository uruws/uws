// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main.
package main

import (
	"flag"
	"fmt"

	"uws/config"
	"uws/log"
)

func main() {
	log.Init("uwscfg")
	var filename string
	flag.StringVar(&filename, "file", "", "load file `name`")
	flag.Parse()

	if filename != "" {
		if err := config.Load(filename); err != nil {
			log.Fatal("%s", err)
		}
	}

	if flag.NArg() > 0 {
		for _, getVar := range flag.Args() {
			fmt.Printf("%s\n", config.Get(getVar))
		}
	} else {
		for _, k := range config.List() {
			fmt.Printf("%s=\"%s\"\n", k, config.Get(k))
		}
	}
}
