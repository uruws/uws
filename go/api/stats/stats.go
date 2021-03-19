// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements api stats manager.
package stats

import (
	"bufio"
	"encoding/json"
	"io"
	"io/ioutil"
	"regexp"
	"strconv"
	"strings"

	"uws/log"
)

var fieldRe = regexp.MustCompile(`\W`)

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	f = strings.TrimSpace(f)
	return fieldRe.ReplaceAllString(f, "_")
}

type Stat struct {
	Name  string `json:"name"`
	Took  int64 `json:"took"`
	Label string `json:"label"`
}

type Info struct {
	session int64
	script  string
	next    int
	R       map[int]*Stat `json:"stats"`
}

func (s *Info) Get(id int) (*Stat, bool) {
	st, ok := s.R[id]
	return st, ok
}

func (s *Info) Len() int {
	return len(s.R)
}

func (s *Info) Add(apiMethod, elapsedTime string) {
	i, err := strconv.ParseInt(elapsedTime, 10, 64)
	if err != nil {
		log.Fatal("%s", err)
	}
	s.R[s.next] = &Stat{Name: cleanFieldName(apiMethod), Took: i,
		Label: apiMethod}
	s.next += 1
}

type Reg struct {
	R map[string]*Info `json:"scripts"`
}

func NewReg() *Reg {
	return &Reg{R: make(map[string]*Info)}
}

func (s *Reg) Len() int {
	return len(s.R)
}

func (s *Reg) newStat(session int64, script string) *Info {
	return &Info{
		session: session,
		script: script,
		next: 0,
		R: make(map[int]*Stat),
	}
}

// List returns the list of script names.
func (s *Reg) List() []string {
	l := make([]string, s.Len())
	idx := 0
	for k := range s.R {
		l[idx] = k
		idx += 1
	}
	return l
}

// Get returns the stats info for script name. Returns bool flag to check if it was found.
func (s *Reg) Get(script string) (*Info, bool) {
	st, ok := s.R[script]
	return st, ok
}

func (s *Reg) get(session, script string) *Info {
	sid, err := strconv.ParseInt(session, 10, 64)
	if err != nil {
		log.Fatal("%s", err)
	}
	if st, ok := s.R[script]; ok {
		if st.session >= sid {
			return st
		}
	}
	return s.newStat(sid, script)
}

func (s *Reg) add(st *Info) {
	s.R[st.script] = nil
	s.R[st.script] = st
}

func (s *Reg) Encode() []byte {
	blob, err := json.MarshalIndent(s, "", "  ")
	//~ blob, err := json.Marshal(s)
	if err != nil {
		log.Fatal("stats encode: %s", err)
	}
	return blob
}

func (s *Reg) String() string {
	return string(s.Encode())
}

var (
	reDocker = regexp.MustCompile(`^([^ ]+) PARSER_([\w/-]+)_([0-9]+)_([\w-]+)-([0-9]+)_ENDPARSER$`)
	reHeroku = regexp.MustCompile(`^([^ ]+) ([^:]+): PARSER_([\w/-]+)_([0-9]+)_([\w-]+)-([0-9]+)_ENDPARSER$`)
)

// Scan checks for lines newer than check time stamp and adds new ones to stats reg.
func Scan(stats *Reg, kind, check string, fh io.Reader) (string, error) {
	var re *regexp.Regexp
	last := check[:]
	log.Debug("scan last '%s'", last)
	if kind == "heroku" {
		re = reHeroku
	} else {
		re = reDocker
	}
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
				st := stats.get(sessionId, scriptName)
				st.Add(apiMethod, elapsedTime)
				stats.add(st)
				last = tstamp
			}
		}
	}
	return last, nil
}

// Load loads stats info from filename to stats reg.
func Load(st *Reg, filename string) error {
	blob, err := ioutil.ReadFile(filename)
	if err != nil {
		return err
	}
	return json.Unmarshal(blob, st)
}
