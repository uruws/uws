// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"context"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"uws/log"
)

type MongoDB struct {
	stats *scriptStats
	ttl   time.Duration
}

func mongodbModule(b *Bot) {
	db := &MongoDB{
		stats: b.stats,
		ttl:   30 * time.Second,
	}
	//uwsdoc: -----
	//uwsdoc: mongodb module:
	if m, err := b.env.Env.NewModule("mongodb"); err != nil {
		log.Fatal("mongodb module: %s", err)
	} else {
		//uwsdoc: db.ping()
		//uwsdoc: 	Checks connection database.
		check(m.Define("ping", db.Ping))
	}
}

// Ping checks database connection.
func (m *MongoDB) Ping(uri string) bool {
	log.Debug("ping")
	ctx, cancel := context.WithTimeout(context.Background(), m.ttl)
	defer cancel()
	st := m.stats.New("mongodb", "ping")
	defer m.stats.Save(st)
	opts := options.Client().ApplyURI(uri)
	cli, err := mongo.Connect(ctx, opts)
	if err != nil {
		st.SetError()
		log.Error("connect: %s", err)
		return false
	}
	if err = cli.Ping(ctx, nil); err != nil {
		st.SetError()
		log.Error("ping: %s", err)
		return false
	}
	return true
}
