// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements api-logs cmd.
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"io"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"

	"uws/log"
)

func main() {
	log.Init("api-logs")
	var (
		statedir string = filepath.FromSlash("/uws/var/api/logs")
		logsdir  string = filepath.FromSlash("/uws/var/api/logs")
		statsdir string = filepath.FromSlash("/uws/var/api/stats")
		env      string = "default"
		filter   string = ""
	)
	flag.StringVar(&statedir, "statedir", statedir, "directory `where` to keep state info")
	flag.StringVar(&logsdir, "logsdir", logsdir, "directory `where` to read logs from")
	flag.StringVar(&statsdir, "statsdir", statsdir, "directory `where` to keep stats info")
	flag.StringVar(&env, "env", env, "env `name`")
	flag.StringVar(&filter, "filter", filter, "filter log `file`")
	flag.Parse()

	lastfn := filepath.Join(filepath.Clean(statedir), filepath.Clean(env), ".api-logs.last")
	last := ""
	if blob, err := ioutil.ReadFile(lastfn); err != nil {
		log.Debug("read lastfn: %s", err)
	} else {
		last = strings.TrimSpace(string(blob))
	}

	var err error
	if filter != "" {
		last, err = Filter(last, filter, logsdir, env)
	}
	if err != nil {
		log.Fatal("%s", err)
	}
	if err := ioutil.WriteFile(lastfn, []byte(last), 0660); err != nil {
		log.Fatal("%s", err)
	}
}

type stat struct {
	script string
	next   int
	R      map[int]map[string]int64 `json:"stats"`
}

func (s *stat) Add(apiMethod, elapsedTime string) {
	i, err := strconv.ParseInt(elapsedTime, 10, 64)
	if err != nil {
		log.Fatal("%s", err)
	}
	s.R[s.next] = map[string]int64{apiMethod: i}
	s.next += 1
}

type statsreg struct {
	R map[string]*stat `json:"scripts"`
}

func newStatsreg() *statsreg {
	return &statsreg{R: make(map[string]*stat)}
}

func (s *statsreg) Len() int {
	return len(s.R)
}

func (s *statsreg) New(script string) *stat {
	return &stat{
		script: script,
		next: 0,
		R: make(map[int]map[string]int64),
	}
}

func (s *statsreg) Add(st *stat) {
	s.R[st.script] = nil
	s.R[st.script] = st
}

func (s *statsreg) String() string {
	blob, err := json.MarshalIndent(s, "", "  ")
	if err != nil {
		log.Fatal("%s", err)
	}
	return string(blob)
}

// Filter parses log lines from filename (stdin if - provided) and avoid duplicates from previous runs.
func Filter(last, filename, logsdir, env string) (string, error) {
	var fh *os.File
	var err error
	stats := newStatsreg()
	if filename == "-" {
		last, err = scan(stats, last, os.Stdin)
	} else {
		fn := filepath.Join(filepath.Clean(logsdir),
			filepath.Clean(env), filepath.Clean(filename))
		fh, err = os.Open(fn)
		if err != nil {
			return "", err
		}
		defer fh.Close()
		last, err = scan(stats, last, fh)
	}
	if err != nil {
		return "", err
	}
	if stats.Len() > 0 {
		log.Debug("%s %d", stats, stats.Len())
	}
	return last, err
}

var re = regexp.MustCompile(`^([^ ]+) ([^:]+): PARSER_([^_]+)_([0-9]+)_([\w-]+)-([0-9]+)_ENDPARSER$`)

func scan(stats *statsreg, check string, fh io.Reader) (string, error) {
	last := check[:]
	log.Debug("scan last '%s'", last)
	x := bufio.NewScanner(fh)
	for x.Scan() {
		line := x.Text()
		m := re.FindStringSubmatch(line)
		if len(m) == 7 {
			tstamp := m[1]
			//tag := m[2]
			apiMethod := m[3]
			elapsedTime := m[4]
			scriptName := m[5]
			sessionId := m[6]
			if last == "" || tstamp > last {
				log.Debug("%s %s %s %s %s", tstamp, sessionId, scriptName, apiMethod, elapsedTime)
				st := stats.New(scriptName)
				st.Add(apiMethod, elapsedTime)
				stats.Add(st)
				last = tstamp
			}
		}
	}
	return last, nil
}
