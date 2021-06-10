// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements uwsca util.
package main

import (
	"fmt"
	"flag"
	"net/http"
	"os"
	"path/filepath"

	"uws/log"
	"uws/wapp"
)

var tplDir string
var port int

func main() {
	log.Init("uwsca")
	log.Debug("init")

	flag.StringVar(&tplDir, "tpldir", filepath.FromSlash("./wapp/tpl"), "templates dir")
	flag.IntVar(&port, "port", 2801, "tcp port to bind to")
	flag.Parse()

	if err := wapp.LoadTemplates(tplDir); err != nil {
		log.Error("%s", err)
		os.Exit(1)
	}

	http.HandleFunc("/", mainHandler)

	log.Debug("listen http://0.0.0.0:%d/", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil); err != nil {
		log.Error("%s", err)
	}
	log.Debug("end")
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	p := wapp.NewPage("ca/index.html")
	p.Title = "uwsca"
	wapp.Render(w, p)
}
