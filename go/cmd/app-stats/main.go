// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package main implements app-stats cmd.
package main

import (
	"flag"
	"os"
	"strings"

	"uws/tapo/app/stats"
	"uws/log"
)

func main() {
	log.Init("app-stats")

	db_name := strings.TrimSpace(os.Getenv("MONGO_DB_NAME"))
	if db_name == "" {
		log.Fatal("MONGO_DB_NAME not set")
	}
	db_uri := strings.TrimSpace(os.Getenv("MONGO_DB_URI"))
	if db_uri == "" {
		log.Fatal("MONGO_DB_URI not set")
	}

	env := strings.TrimSpace(os.Getenv("app_env"))
	if env == "" {
		env = "default"
	}
	flag.StringVar(&env, "env", env, "env `name`")

	flag.Parse()

	var err error

	cmd := flag.Arg(0)

	if cmd == "config" {
		err = Config(env)
	} else {
		cmd = "report"
		db := stats.NewDB(db_name)
		err = db.Connect(db_uri)
		if err == nil {
			err = Report(db, env)
		}
	}

	if err != nil {
		log.Fatal("app stats %s: %s", cmd, err)
	}
}

// Config generates munin plugin config output.
func Config(env string) error {
	log.Debug("%s: config", env)
	stats.ActiveSessionsConfig(env)
	return nil
}

// Report prints munin plugin values.
func Report(m *stats.MDB, env string) error {
	log.Debug("%s: report", env)
	stats.ActiveSessions(m, env)
	return nil
}
