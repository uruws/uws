// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements api job stats manager.
package stats

import (
	"context"
	"regexp"
	"strings"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"uws/log"
)

var fieldRe = regexp.MustCompile(`\W`)

func cleanFieldName(n ...string) string {
	f := strings.Join(n, "_")
	f = strings.TrimSpace(f)
	return fieldRe.ReplaceAllString(f, "_")
}

type Job struct {
	ID      string
	Name    string
	Label   string
	Error   bool
	Waiting int64
	Ready   int64
	Running int64
	Failed  int64
	Took    int64
	start   time.Time
}

func newJob(collection string) *Job {
	return &Job{
		ID:    cleanFieldName(collection),
		Name:  collection,
		Label: collection,
		Error: true,
		start: time.Now(),
	}
}

type Stats struct {
	db_name string
	db_uri  string
	r       map[string]*Job
}

func New(db_name, db_uri string) *Stats {
	log.Debug("new")
	return &Stats{db_name: db_name, db_uri: db_uri, r: make(map[string]*Job)}
}

func (s *Stats) Len() int {
	return len(s.r)
}

func (s *Stats) List() []*Job {
	log.Debug("list")
	l := make([]*Job, 0)
	for _, j := range s.r {
		l = append(l, j)
	}
	return l
}

func (s *Stats) Fetch() int {
	errcount := 0
	log.Debug("fetch")
	db := newDB(s.db_name)
	if err := db.Connect(s.db_uri); err != nil {
		log.Error("%v", err)
		return 1
	}
	defer db.Disconnect()
	cols, err := db.Collections()
	if err != nil {
		log.Error("%v", err)
		return 1
	}
	for _, c := range cols {
		job := newJob(c)
		if err := db.Get(job); err != nil {
			log.Error("%v", err)
			errcount += 1
		} else {
			job.Error = false
			job.Took = time.Now().Sub(job.start).Milliseconds()
			s.r[c] = job
		}
	}
	return errcount
}

func (s *Stats) Config() error {
	log.Debug("config")
	db := newDB(s.db_name)
	if err := db.Connect(s.db_uri); err != nil {
		return log.DebugError(err)
	}
	defer db.Disconnect()
	cols, err := db.Collections()
	if err != nil {
		return log.DebugError(err)
	}
	for _, c := range cols {
		s.r[c] = newJob(c)
	}
	return nil
}

type mdb struct {
	ctx    context.Context
	cancel context.CancelFunc
	cli    *mongo.Client
	name   string
	db     *mongo.Database
}

func newDB(name string) *mdb {
	ttl := 3 * time.Minute
	ctx, cancel := context.WithTimeout(context.Background(), ttl)
	return &mdb{ctx: ctx, cancel: cancel, name: name}
}

func (m *mdb) Connect(db_uri string) error {
	var err error
	opts := options.Client().ApplyURI(db_uri)
	m.cli, err = mongo.Connect(m.ctx, opts)
	if err != nil {
		return log.DebugError(err)
	}
	m.db = m.cli.Database(m.name, options.Database())
	return m.cli.Ping(m.ctx, nil)
}

func (m *mdb) Disconnect() {
	defer m.cancel()
	if m.cli != nil {
		if err := m.cli.Disconnect(m.ctx); err != nil {
			log.Error("%v", err)
		}
	}
}

func (m *mdb) Collections() ([]string, error) {
	opts := options.ListCollections()
	opts.SetNameOnly(true)
	l := make([]string, 0)
	cl, err := m.db.ListCollectionNames(m.ctx, bson.D{}, opts)
	if err != nil {
		return l, err
	}
	for _, cn := range cl {
		if strings.HasSuffix(cn, ".jobs") {
			l = append(l, cn)
		}
	}
	return l, nil
}

func (m *mdb) Get(job *Job) error {
	coll := m.db.Collection(job.Name, options.Collection())
	opts := options.Count()
	opts.SetMaxTime(15 * time.Second)
	var err error
	job.Waiting, err = coll.CountDocuments(m.ctx, bson.D{{"status", "waiting"}}, opts)
	if err != nil {
		return log.DebugError(err)
	}
	job.Ready, err = coll.CountDocuments(m.ctx, bson.D{{"status", "ready"}}, opts)
	if err != nil {
		return log.DebugError(err)
	}
	job.Running, err = coll.CountDocuments(m.ctx, bson.D{{"status", "running"}}, opts)
	if err != nil {
		return log.DebugError(err)
	}
	job.Failed, err = coll.CountDocuments(m.ctx, bson.D{{"status", "failed"}}, opts)
	if err != nil {
		return log.DebugError(err)
	}
	return nil
}
