// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsca util.
package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"path/filepath"

	"uws/log"
	"uws/wapp"
	"uws/wapp/view/ca"
)

var (
	tplDir string
	stDir  string
	port   int
)

func main() {
	log.Init("uwsca")
	log.Debug("init")

	flag.StringVar(&tplDir, "tpldir", filepath.FromSlash("./wapp/tpl"), "templates dir")
	flag.StringVar(&stDir, "stdir", filepath.FromSlash("./wapp/static"), "static files dir")
	flag.IntVar(&port, "port", 2801, "tcp port to bind to")
	flag.Parse()

	if err := wapp.LoadTemplates(tplDir, "ca"); err != nil {
		log.Error("%s", err)
		os.Exit(1)
	}

	wapp.ServeStatic(stDir)
	http.HandleFunc("/", ca.Index)

	log.Debug("listen http://0.0.0.0:%d/", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil); err != nil {
		log.Error("%s", err)
	}
	log.Debug("end")
}
