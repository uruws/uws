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
	fmt.Println("start...")
	http.HandleFunc("/", mainHandler)
	http.ListenAndServe(":2800", nil)
	fmt.Println("end!")
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
	if hostname, err := os.Hostname(); err != nil {
		fmt.Println("[ERROR]", err)
		fmt.Fprintf(w, "ERROR: %s\n", err)
	} else {
		fmt.Println(r.RemoteAddr, r.RequestURI, hostname)
		fmt.Fprintf(w, "%s\n", hostname)
	}
}
