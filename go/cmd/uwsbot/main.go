// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package main.
package main

import (
	"uws/env"
	"uws/log"
)

func main() {
	log.Init("uwsbot")
	botEnv := env.Get("BOT")
	if botEnv == "" {
		log.Fatal("ERR: bot env not set")
	}
	if err := env.Load("bot", botEnv); err != nil {
		log.Debug("%v", err)
	}
}
