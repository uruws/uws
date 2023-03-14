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
	Errors bool
	Input  string
	Raw    bool
}

func NewFlags() *Flags {
	return &Flags{
		Input: "-",
	}
}

func Main(f *Flags) {
	log.Debug("main: errors=%v raw=%v", f.Errors, f.Raw)

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

	if f.Raw {
		err = rawOutput(infh)
	} else {
		err = jsonParse(f, infh)
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
	rePod = `^\[pod/proxy-([^/]+/ngx\d+)\] `
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
	f              *Flags
	Container      string `json:"-"`
	Request        string `json:"request"`
	RequestMethod  string `json:"request_method"`
	RequestTime    string `json:"request_time"`
	RequestURI     string `json:"request_uri"`
	Status         string `json:"status"`
	StatusInt      int    `json:"-"`
	TimeLocal      string `json:"time_local"`
	UpstreamName   string `json:"upstream_name"`
	UpstreamStatus string `json:"upstream_status"`
	UpstreamTime   string `json:"upstream_response_time"`
}

func newEntry(f *Flags, container string) *Entry {
	return &Entry{
		f:         f,
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
	show := true
	if e.StatusInt >= 500 {
		p = log.PrintError
	} else if e.StatusInt >= 400 {
		p = log.Warn
	} else if e.f.Errors {
		show = false
	}
	if show {
		p("%s [%s %s %s] %s %s %s %s", e.TimeLocal[:len(e.TimeLocal)-6], e.UpstreamName, e.UpstreamTime, e.UpstreamStatus, e.RequestTime, e.Status, e.RequestMethod, e.RequestURI)
	}
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
			e := newEntry(f, container)
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
