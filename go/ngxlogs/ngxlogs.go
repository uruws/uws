// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ngxlogs provides tools to interact with nginx server logs.
package ngxlogs

import (
	"bufio"
	"encoding/json"
	"io"
	"os"
	"regexp"
	"strconv"

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
	rePod = `^\[pod/proxy-([^/]+)/proxy\] `
)

var (
	reJsonLog  = regexp.MustCompile(rePod + `(\{.+\})$`)
	reErrorLog = regexp.MustCompile(rePod + `(\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d) \[error\] (.+)$`)
	reStartLog = regexp.MustCompile(rePod + `nginx: start (.+)$`)
)

//
// jsonParse
//

type Entry struct {
	Container  string `json:"-"`
	RequestURI string `json:"request_uri"`
	Status     string `json:"status"`
	StatusInt  int    `json:"-"`
	TimeLocal  string `json:"time_local"`
}

func newEntry(container string) *Entry {
	return &Entry{
		Container: container,
	}
}

func (e *Entry) Check() bool {
	var err error
	e.StatusInt, err = strconv.Atoi(e.Status)
	if err != nil {
		log.Print("[ERROR] e.Status: %s", err)
		return false
	}
	return true
}

func (e *Entry) Print() {
	var p func(string, ...interface{})
	p = log.Info
	if e.StatusInt >= 500 {
		p = log.PrintError
	} else if e.StatusInt >= 400 {
		p = log.Warn
	}
	p("%s %s %s %s", e.TimeLocal, e.Container, e.Status, e.RequestURI)
}

func jsonParse(f *Flags, r io.Reader) error {
	log.Debug("json parse")
	x := bufio.NewScanner(r)
	for x.Scan() {
		s := x.Text()
		//~ log.Debug("%s", s)
		m := reJsonLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			data := m[2]
			e := newEntry(container)
			if err := json.Unmarshal([]byte(data), e); err != nil {
				log.Print("[ERROR] %s", err)
				continue
			}
			if !e.Check() {
				continue
			}
			e.Print()
			continue
		}
		m = reErrorLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			time := m[2]
			msg := m[3]
			log.Print("[ERROR] %s %s %s", time, container, msg)
			continue
		}
		m = reStartLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			time := m[2]
			log.Print("%s container start %s", time, container)
			continue
		}
	}
	return x.Err()
}
