// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ngxlogs provides tools to interact with nginx server logs.
package ngxlogs

import (
	"bufio"
	"io"
	"os"
	"regexp"

	"uws/log"
)

type Flags struct {
	Input  string
	Format string
}

func NewFlags() *Flags {
	return &Flags{
		Input:  "-",
		Format: "default",
	}
}

func Main(f *Flags) {
	log.Debug("main: %s", f.Format)

	var (
		err  error
		infh *os.File
	)
	if f.Input == "-" {
		infh = os.Stdin
	} else {
		infh, err = os.Open(f.Input)
		if err != nil {
			log.Fatal("%s", err)
		}
		defer infh.Close()
	}

	if f.Format == "json" {
		err = jsonParse(f, infh)
	} else if f.Format == "raw" {
		err = rawOutput(infh)
	}

	if err != nil {
		log.Fatal("%s", err)
	}
}

//
// rawOutput
//

func rawOutput(r io.Reader) error {
	log.Debug("raw output")
	x := bufio.NewScanner(r)
	for x.Scan() {
		log.Print("%s", x.Text())
	}
	return x.Err()
}

//
// regexp
//

var (
	rePod = `^\[pod/proxy-[^/]+/proxy\] `
)

var (
	reJsonLog  = regexp.MustCompile(rePod + `\{.*\}$`)
	reErrorLog = regexp.MustCompile(rePod + `\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d \[error\] `)
	reStartLog = regexp.MustCompile(rePod + `nginx: start`)
)

//
// jsonParse
//

func jsonParse(f *Flags, r io.Reader) error {
	log.Debug("json parse")
	x := bufio.NewScanner(r)
	for x.Scan() {
		log.Info("%s", x.Text())
	}
	return x.Err()
}
