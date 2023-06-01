// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package ngxlogs provides tools to parse json analytics nginx server logs.
package ngxlogs

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"

	"uws/log"
)

//
// Main
//

type Flags struct {
	Errors bool
	Input  string
	Raw    bool
	Stats  bool
}

func NewFlags() *Flags {
	return &Flags{
		Input: "-",
		Stats: true,
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
		p := jsonParse(f, infh)
		err = p.Error
		if f.Stats {
			p.PrintStats()
		}
	}

	if err != nil {
		log.Fatal("%s", err)
	}
}

//
// rawOutput
//

var rawOutput = func(r io.Reader) error {
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
// Entry
//

type Entry struct {
	f              *Flags
	ok             bool
	Container      string `json:"-"`
	RemoteAddr     string `json:"remote_addr"`
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
		Status:    "0",
		TimeLocal: " +0000",
	}
}

func (e *Entry) Check() bool {
	var err error
	e.StatusInt, err = strconv.Atoi(e.Status)
	if err != nil {
		log.Print("[ERROR] e.Status: %s", err)
		return false
	}
	e.ok = true
	return e.ok
}

func (e *Entry) Print() bool {
	if !e.ok {
		return false
	}
	var p func(string, ...interface{})
	p = log.Info
	show := true
	if e.StatusInt >= 500 {
		p = log.PrintError
	} else if e.StatusInt == 499 {
		p = log.Print
	} else if e.StatusInt >= 400 {
		p = log.Warn
	} else if e.StatusInt < 200 {
		p = log.Print
		if e.f.Errors {
			show = false
		}
	} else if e.f.Errors {
		show = false
	}
	if show {
		p("%s %s %-15s [%s %s %s] %s %s %s %s",
			e.TimeLocal[:len(e.TimeLocal)-6],
			e.Container,
			e.RemoteAddr,

			e.UpstreamName,
			e.UpstreamTime,
			e.UpstreamStatus,

			e.RequestTime,
			e.Status,
			e.RequestMethod,
			e.RequestURI,
		)
	}
	return show
}

//
// Stats
//

type Stats struct {
	NgxErrors int
	NgxStarts int
	Requests  int
	OK        int
	Warning   int
	Error     int
	Websocket int
}

func newStats() *Stats {
	return &Stats{}
}

func (s *Stats) Print(w io.Writer) {
	fmt.Fprintf(w, "%s", "Nginx\n")
	fmt.Fprintf(w, "  Server starts : %d\n", s.NgxStarts)
	fmt.Fprintf(w, "  Server errors : %d\n", s.NgxErrors)
	fmt.Fprintf(w, "  Requests      : %d\n", s.Requests)
	fmt.Fprintf(w, "    OK          : %d\n", s.OK)
	fmt.Fprintf(w, "    Warning     : %d\n", s.Warning)
	fmt.Fprintf(w, "    Errror      : %d\n", s.Error)
	fmt.Fprintf(w, "  Websocket     : %d\n", s.Websocket)
}

//
// jsonParse
//

type Parser struct {
	stats      bool
	Stats      *Stats
	Error      error
	Lines      int
	Read       int
	LinesError int
	Unknown    int
}

func newParser(stats bool) *Parser {
	return &Parser{stats: stats, Stats: newStats()}
}

func (p *Parser) PrintStats() bool {
	if !p.stats {
		return false
	}
	w := log.Writer()
	fmt.Fprintf(w, "%s", "\n")
	fmt.Fprintf(w, "%s", "Parser\n")
	fmt.Fprintf(w, "  Error        : %v\n", p.Error != nil)
	fmt.Fprintf(w, "  Lines        : %d\n", p.Lines)
	fmt.Fprintf(w, "  Lines read   : %d\n", p.Read)
	fmt.Fprintf(w, "  Lines error  : %d\n", p.LinesError)
	fmt.Fprintf(w, "  Lines ignore : %d\n", p.Unknown)
	fmt.Fprintf(w, "%s", "\n")
	p.Stats.Print(w)
	fmt.Fprintf(w, "%s", "\n")
	return true
}

func (p *Parser) Count(e *Entry) {
	p.Read += 1
	if !p.stats {
		return
	}
	p.Stats.Requests += 1
	if e.StatusInt >= 500 {
		p.Stats.Error += 1
	} else if e.StatusInt >= 400 {
		p.Stats.Warning += 1
	} else {
		p.Stats.OK += 1
	}
	if e.StatusInt == 101 {
		p.Stats.Websocket += 1
	}
}

func (p *Parser) CountNgxError() {
	p.Read += 1
	if !p.stats {
		return
	}
	p.Stats.NgxErrors += 1
}

func (p *Parser) CountNgxStart() {
	p.Read += 1
	if !p.stats {
		return
	}
	p.Stats.NgxStarts += 1
}

func jsonParse(f *Flags, r io.Reader) *Parser {
	log.Debug("json parse")
	p := newParser(f.Stats)
	x := bufio.NewScanner(r)
	for x.Scan() {
		s := x.Text()
		//~ log.Debug("%s", s)
		p.Lines += 1
		// request info
		m := reJsonLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			data := m[2]
			e := newEntry(f, container)
			if err := json.Unmarshal([]byte(data), e); err != nil {
				log.Print("[ERROR] %s", err)
				p.LinesError += 1
				continue
			}
			if !e.Check() {
				p.LinesError += 1
				continue
			}
			e.Print()
			p.Count(e)
			continue
		}
		// nginx server error log
		m = reErrorLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			time := m[2]
			msg := m[3]
			log.Print("[ERROR] %s %s %s", time, container, msg)
			p.CountNgxError()
			continue
		}
		// nginx server start
		m = reStartLog.FindStringSubmatch(s)
		if len(m) > 1 {
			container := m[1]
			time := m[2]
			log.Print("%s %s container start", time, container)
			p.CountNgxStart()
			continue
		}
		// unknown log entry
		p.Unknown += 1
	}
	p.Error = x.Err()
	return p
}
