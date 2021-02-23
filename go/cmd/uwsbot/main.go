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
		log.Fatal("ERR: bot not set")
	}
	if err := env.Load(botEnv); err != nil {
		log.Fatal("%v", err)
	}
}
