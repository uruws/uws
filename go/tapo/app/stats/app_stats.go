// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package stats implements app stats manager.
package stats

import (
	"context"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"uws/log"
)

type MDB struct {
	ctx    context.Context
	cancel context.CancelFunc
	cli    *mongo.Client
	name   string
	db     *mongo.Database
}

func NewDB(name string) *MDB {
	return &MDB{name: name}
}

func (m *MDB) Connect(db_uri string) error {
	var err error
	ttl := 3 * time.Minute
	opts := options.Client().ApplyURI(db_uri)
	m.ctx, m.cancel = context.WithTimeout(context.Background(), ttl)
	m.cli, err = mongo.Connect(m.ctx, opts)
	if err != nil {
		return log.DebugError(err)
	}
	m.db = m.cli.Database(m.name, options.Database())
	return m.cli.Ping(m.ctx, nil)
}

func (m *MDB) Disconnect() {
	defer m.cancel()
	if m.cli != nil {
		if err := m.cli.Disconnect(m.ctx); err != nil {
			log.Error("%v", err)
		}
	}
}

func (m *MDB) CountAll(cn string) (int64, error) {
	coll := m.db.Collection(cn, options.Collection())
	opts := options.Count()
	opts.SetMaxTime(15 * time.Second)
	return coll.CountDocuments(m.ctx, bson.D{}, opts)
}

func ActiveSessionsConfig(env string) {
	fmt.Printf("multigraph appstats_%s_active_sessions\n", env)
	fmt.Printf("graph_title %s app active sessions\n", env)
	fmt.Println("graph_args --base 1000 -l 0")
	fmt.Println("graph_vlabel active sessions")
	fmt.Println("graph_category app")
	fmt.Println("graph_scale no")
	fmt.Println("graph_printf %3.0lf")
	fmt.Println("f0_active_sessions.label active sessions")
	fmt.Println("f0_active_sessions.draw AREASTACK")
	fmt.Println("f0_active_sessions.colour COLOUR0")
	fmt.Println("f0_active_sessions.min 0")
}

func ActiveSessions(m *MDB, env string) {
	fmt.Printf("multigraph appstats_%s_active_sessions\n", env)
	if as, err := m.CountAll("activeSessions"); err != nil {
		log.Error("%s app count active sessions: %s", env, err)
		fmt.Println("f0_active_sessions.value U")
	} else {
		fmt.Printf("f0_active_sessions.value %d\n", as)
	}
}
