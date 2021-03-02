// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements bot stats generator/manager.
package stats

import (
	"container/list"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"uws/env"
	"uws/fs"
	"uws/log"
)

var (
	fieldRe *regexp.Regexp
)

func init() {
	// regexp: \W not word characters (== [^0-9A-Za-z_])
	fieldRe = regexp.MustCompile(`\W`)
}

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	f = strings.TrimSpace(f)
	return fieldRe.ReplaceAllString(f, "_")
}

type Stats struct {
	id     string
	stdir  string
	fname  string
	label  string
	tmpdir string
	start  time.Time
	child  bool
	benv   string
	bname  string
	haserr bool
	errval bool
	script string
}

func newStats(fieldName ...string) *Stats {
	stdir := env.GetFilepath("STATSDIR")
	fname := cleanFieldName(fieldName...)
	return &Stats{stdir: stdir, fname: fname, start: time.Now(), errval: true}
}

func New(benv, bname string) *Stats {
	var err error
	st := newStats(benv, bname)
	st.id = st.fname
	st.benv = benv
	st.bname = bname
	st.tmpdir, err = ioutil.TempDir("", "uwsbot-stats-*")
	st.label = fmt.Sprintf("bot/%s %s", st.benv, st.bname)
	if err != nil {
		log.Fatal("stats new: %s", err)
	}
	log.Debug("new %s %s %s %s %s", st.benv, st.bname, st.stdir, st.fname, st.tmpdir)
	return st
}

func NewChild(benv, bname, tmpdir, runfn string) *Stats {
	st := newStats(runfn)
	st.id = cleanFieldName(runfn)
	st.child = true
	st.benv = benv
	st.bname = bname
	st.tmpdir = tmpdir
	st.label = runfn
	log.Debug("child stats")
	return st
}

func NewScript(benv, bname, tmpdir, runfn string, name ...string) *Stats {
	st := NewChild(benv, bname, tmpdir, runfn)
	st.script = runfn
	st.tmpdir = filepath.Join(tmpdir, st.id)
	st.id = cleanFieldName(name...)
	st.fname = cleanFieldName(name...)
	st.label = strings.Join(name, " ")
	log.Debug("script stats")
	return st
}

func (s *Stats) Dirname() string {
	return s.tmpdir
}

func (s *Stats) SetError() {
	s.haserr = true
}

func Save(st *Stats) {
	saveStats(st)
	if st.child {
		return
	}
	dst := filepath.Join(st.stdir, st.fname)
	if err := os.MkdirAll(dst, 0750); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats save: %s", err)
	}
	log.Debug("stats lock %s", dst)
	if err := fs.LockDir(dst); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats lock: %s", err)
	}
	defer fs.UnlockDir(dst)
	log.Debug("stats save remove %s", dst)
	os.RemoveAll(dst)
	log.Debug("stats save: %s -> %s", st.tmpdir, dst)
	// FIXME: stop calling mv command
	// we use mv though because of an issue wiht os.Rename under docker volumes
	rename := exec.Command("mv", "-f", st.tmpdir, dst)
	if err := rename.Run(); err != nil {
		os.RemoveAll(st.tmpdir)
		log.Fatal("stats save: %s", err)
	}
}

type Info struct {
	Id    string `json:"id"`
	Name  string `json:"name"`
	Label string `json:"label"`
	Value int64  `json:"value"`
	Error bool   `json:"error"`
	children *list.List
	fn    string
}

func newInfo() *Info {
	return &Info{children: list.New()}
}

func saveStats(st *Stats) {
	var fn string
	if st.child {
		fn = filepath.Join(st.tmpdir, st.fname+".stats")
	} else {
		fn = filepath.Join(st.tmpdir, "stats")
	}
	log.Debug("save (child:%v) stats %s", st.child, fn)
	if !st.haserr {
		st.errval = false
	}
	inf := &Info{
		Id:    st.id,
		Name:  cleanFieldName(st.benv, st.bname),
		Label: st.label,
		Value: time.Now().Sub(st.start).Milliseconds(),
		Error: st.errval,
	}
	if st.script != "" {
		inf.Name = fmt.Sprintf("%s.%s", inf.Name, cleanFieldName(st.script))
	}
	blob, err := json.Marshal(inf)
	if err != nil {
		log.Fatal("save stats %s: %s", fn, err)
	}
	if err := os.MkdirAll(filepath.Dir(fn), 0750); err != nil {
		log.Error("save stats %s: %s", fn, err)
	}
	if err := ioutil.WriteFile(fn, blob, 0640); err != nil {
		log.Fatal("save stats: %s", err)
	}
}

func loadStats(fn string) (*Info, error) {
	blob, err := ioutil.ReadFile(fn)
	if err != nil {
		return nil, err
	}
	inf := newInfo()
	if err := json.Unmarshal(blob, inf); err != nil {
		return nil, err
	}
	inf.fn = fn
	return inf, nil
}

type Report struct {
	bots    *list.List
	scripts *list.List
}

func newReport() *Report {
	return &Report{
		bots:    list.New(),
		scripts: list.New(),
	}
}

func Parse(stdir, benv, bname string) (*Report, error) {
	if benv == "" || benv == "ALL" {
		benv = "*"
	} else {
		benv = cleanFieldName(benv)
	}
	if bname == "" || bname == "ALL" {
		bname = "*"
	} else {
		bname = cleanFieldName(bname)
	}
	patt := filepath.Clean(stdir)
	patt = filepath.Join(patt, benv+"_"+bname, "stats")
	r := newReport()
	fl, err := filepath.Glob(patt)
	if err != nil {
		return nil, err
	}
	// all bots
	for _, fn := range fl {
		dn := filepath.Dir(fn)
		log.Debug("parse load dir %s", dn)
		patt := filepath.Join(dn, "*.stats")
		sl, err := filepath.Glob(patt)
		if err != nil {
			return nil, err
		}
		log.Debug("parse %s", fn)
		if inf, err := loadStats(fn); err != nil {
			return nil, err
		} else {
			r.bots.PushBack(inf)
		}
		// bot scripts
		for _, sfn := range sl {
			log.Debug("parse %s", sfn)
			inf, err := loadStats(sfn)
			if err != nil {
				return nil, err
			}
			// bot scripts info
			d := sfn[:len(sfn)-6]
			log.Debug("parse load dir %s", d)
			patt := filepath.Join(d, "*.stats")
			l, errx := filepath.Glob(patt)
			if errx != nil {
				return nil, errx
			}
			for _, n := range l {
				log.Debug("parse script info %s", n)
				if i, err := loadStats(n); err != nil {
					return nil, err
				} else {
					log.Debug("loaded %s", i.fn)
					inf.children.PushBack(i)
				}
			}
			r.scripts.PushBack(inf)
		}
	}
	return r, nil
}

var reportDevel bool = true

func (r *Report) Print() {
	// all bots
	fmt.Println("multigraph uwsbot")
	for e := r.bots.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		var v string
		if i.Error {
			v = "U"
		} else {
			v = fmt.Sprintf("%d", i.Value)
		}
		fmt.Println(cleanFieldName(i.Id)+".value", v)
	}
	// all bots errors
	if reportDevel { fmt.Println() }
	fmt.Println("multigraph uwsbot_errors")
	for e := r.bots.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		v := 0
		if i.Error {
			v = 1 // FIXME: count bot errors
		}
		fmt.Printf("errors_%s.value %d\n", cleanFieldName(i.Id), v)
	}
	// bots scripts
	for e := r.scripts.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		var v string
		if reportDevel { fmt.Println() }
		fmt.Printf("multigraph uwsbot_%s\n", i.Name)
		if i.Error {
			v = "U"
		} else {
			v = fmt.Sprintf("%d", i.Value)
		}
		fmt.Println(cleanFieldName(i.Id)+".value", v)
	}
	// bots scripts errors
	for e := r.scripts.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		if reportDevel { fmt.Println() }
		fmt.Printf("multigraph uwsbot_%s\n", i.Name)
		v := 0
		if i.Error {
			v = 1 // FIXME: count bot script errors
		}
		fmt.Printf("errors_%s.value %d\n", cleanFieldName(i.Id), v)
	}
}

func (r *Report) Config() {
	// all bots
	fmt.Println("multigraph uwsbot")
	fmt.Println("graph_title monitoring bots")
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel seconds")
	fmt.Println("graph_category uwsbot")
	fmt.Println("graph_scale no")
	for e := r.bots.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		//~ if reportDevel { fmt.Printf("-- %s\n", i.fn) }
		id := cleanFieldName(i.Id)
		fmt.Println(fmt.Sprintf("%s.label %s", id, i.Label))
		fmt.Println(fmt.Sprintf("%s.min 0", id))
		fmt.Println(fmt.Sprintf("%s.cdef %s,1000,/", id, id))
	}
	// all bots errors
	if reportDevel { fmt.Println() }
	fmt.Println("multigraph uwsbot_errors")
	fmt.Println("graph_title monitoring bots errors")
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel number of errors")
	fmt.Println("graph_category uwsbot")
	fmt.Println("graph_scale no")
	for e := r.bots.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		//~ if reportDevel { fmt.Printf("-- %s\n", i.fn) }
		id := cleanFieldName(i.Id)
		fmt.Printf("errors_%s.label %s errors\n", id, i.Label)
		fmt.Printf("errors_%s.warning 1\n", id)
	}
	// bots scripts
	for e := r.scripts.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		id := cleanFieldName(i.Id)
		if reportDevel { fmt.Println() }
		//~ if reportDevel { fmt.Printf("-- %s\n", i.fn) }
		fmt.Printf("multigraph uwsbot_%s\n", i.Name)
		fmt.Printf("graph_title bot %s\n", i.Name)
		fmt.Println("graph_args --base 1000 -l 0")
		fmt.Println("graph_vlabel seconds")
		fmt.Println("graph_category uwsbot")
		fmt.Println("graph_scale no")
		fmt.Printf("%s.label %s\n", id, i.Label)
		fmt.Printf("%s.min 0\n", id)
		fmt.Printf("%s.warning 60000\n", id)
		fmt.Printf("%s.cdef %s,1000,/\n", id, id)
		// scripts info
		cihead := true
		for c := i.children.Front(); c != nil; c = c.Next() {
			ci := c.Value.(*Info)
			if cihead {
				if reportDevel { fmt.Println() }
				fmt.Printf("multigraph uwsbot_%s\n", ci.Name)
				fmt.Printf("graph_title bot %s\n", ci.Name)
				fmt.Println("graph_args --base 1000 -l 0")
				fmt.Println("graph_vlabel seconds")
				fmt.Println("graph_category uwsbot")
				fmt.Println("graph_scale no")
				cihead = false
			}
			//~ if reportDevel { fmt.Printf("-- %s\n", ci.fn) }
			fmt.Printf("%s.label %s\n", ci.Id, ci.Label)
			fmt.Printf("%s.min 0\n", ci.Id)
			fmt.Printf("%s.warning 60000\n", ci.Id)
			fmt.Printf("%s.cdef %s,1000,/\n", ci.Id, ci.Id)
		}
	}
	// bots scripts errors
	for e := r.scripts.Front(); e != nil; e = e.Next() {
		i := e.Value.(*Info)
		id := cleanFieldName(i.Id)
		if reportDevel { fmt.Println() }
		//~ if reportDevel { fmt.Printf("-- %s\n", i.fn) }
		fmt.Printf("multigraph uwsbot_errors_%s\n", i.Name)
		fmt.Printf("graph_title bot %s errors\n", i.Name)
		fmt.Println("graph_args --base 1000 -l 0")
		fmt.Println("graph_vlabel number of errors")
		fmt.Println("graph_category uwsbot")
		fmt.Println("graph_scale no")
		fmt.Printf("errors_%s.label %s errors\n", id, i.Label)
		fmt.Printf("errors_%s.warning 1\n", id)
		// scripts info
		cihead := true
		for c := i.children.Front(); c != nil; c = c.Next() {
			ci := c.Value.(*Info)
			if cihead {
				if reportDevel { fmt.Println() }
				fmt.Printf("multigraph uwsbot_errors_%s\n", ci.Name)
				fmt.Printf("graph_title bot %s\n", ci.Name)
				fmt.Println("graph_args --base 1000 -l 0")
				fmt.Println("graph_vlabel number of errors")
				fmt.Println("graph_category uwsbot")
				fmt.Println("graph_scale no")
				cihead = false
			}
			//~ if reportDevel { fmt.Printf("-- %s\n", ci.fn) }
			fmt.Printf("errors_%s.label %s errors\n", ci.Id, ci.Label)
			fmt.Printf("errors_%s.warning 1\n", ci.Id)
		}
	}
}
