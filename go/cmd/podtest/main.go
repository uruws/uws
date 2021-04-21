// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements podtest util.
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/", mainHandler)
	http.ListenAndServe(":8699", nil)
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		fmt.Fprintf(w, "ERROR: %s\n", err)
	} else {
		fmt.Fprintf(w, "%s\n", hostname)
	}
}
