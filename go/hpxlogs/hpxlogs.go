// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package hpxlogs provides tools to parse json analytics haproxy server logs.
package hpxlogs

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"regexp"

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
	reJsonLog = regexp.MustCompile(`^\d[^\{]*(\{.+\})$`)
)

//
// Entry
//

type Entry struct {
	f                *Flags
	ok               bool
	ActiveConn       int    `json:"active_conn"`
	ActiveTime       int    `json:"active_time"`
	BackendConn      int    `json:"backend_conn"`
	Backend          string `json:"backend"`
	Client           string `json:"client"`
	ClientPort       int    `json:"client_port"`
	ClientTime       int    `json:"client_time"`
	Datetime         string `json:"datetime"`
	Frontend         string `json:"frontend"`
	FrontendConn     int    `json:"frontend_conn"`
	Hostname         string `json:"hostname"`
	HttpVersion      string `json:"http_version"`
	Id               string `json:"id"`
	Method           string `json:"method"`
	Path             string `json:"path"`
	ReqBytes         int    `json:"req_bytes"`
	RespBytes        int    `json:"resp_bytes"`
	RespTime         int    `json:"resp_time"`
	Retries          int    `json:"retries"`
	Server           string `json:"server"`
	ServerConn       int    `json:"server_conn"`
	Status           int    `json:"status"`
	TerminationState string `json:"termination_state"`
	Timestamp        uint   `json:"timestamp"`
}

func newEntry(f *Flags) *Entry {
	return &Entry{
		f: f,
	}
}

func (e *Entry) Check() bool {
	if e.Status == 0 {
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
	if e.Status >= 500 {
		p = log.PrintError
	} else if e.Status >= 400 {
		p = log.Warn
	} else if e.Status < 200 {
		p = log.Print
		if e.f.Errors {
			show = false
		}
	} else if e.f.Errors {
		show = false
	}
	if show {
		p("%s %s %-15s %5d [%s %5d] %5d %3d %s %s",
			e.Datetime,
			e.Frontend,
			e.Client,
			e.ClientTime,

			e.Server,
			e.ActiveTime,

			e.RespTime,
			e.Status,
			e.Method,
			e.Path,
		)
	}
	return show
}

//
// Stats
//

type Stats struct {
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
	if e.Status >= 500 {
		p.Stats.Error += 1
	} else if e.Status >= 400 {
		p.Stats.Warning += 1
	} else {
		p.Stats.OK += 1
	}
	if e.Status == 101 {
		p.Stats.Websocket += 1
	}
}

func jsonParse(f *Flags, r io.Reader) *Parser {
	log.Debug("json parse")
	p := newParser(f.Stats)
	x := bufio.NewScanner(r)
	for x.Scan() {
		s := x.Text()
		p.Lines += 1
		// request json info
		//~ println(s)
		m := reJsonLog.FindStringSubmatch(s)
		//~ println(len(m))
		if len(m) == 2 {
			data := m[1]
			e := newEntry(f)
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
		// unknown log entry
		p.Unknown += 1
	}
	p.Error = x.Err()
	return p
}
