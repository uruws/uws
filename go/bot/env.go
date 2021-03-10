// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"uws/log"

	"github.com/mattn/anko/env"
)

type botEnv struct {
	*env.Env
}

func newBotEnv() *botEnv {
	return &botEnv{
		Env: envDefine(),
	}
}

func check(err error) {
	if err != nil {
		log.Fatal("bot env define: %s", err)
	}
}

func envDefine() *env.Env {
	//uwsdoc: -----
	//uwsdoc: log module:
	e := env.NewEnv()
	if logm, err := e.NewModule("log"); err != nil {
		log.Fatal("bot env log module: %s", err)
	} else {
		//uwsdoc: log.fatal(format, message)
		//uwsdoc: 	Prints an error message and aborts execution with an error
		//uwsdoc: 	status.
		check(logm.Define("fatal", log.Fatal))
		//uwsdoc: log.debug(format, message)
		//uwsdoc: 	Prints debug messages. Only printed when debug is enabled.
		check(logm.Define("debug", log.Debug))
		//uwsdoc: log.error(format, message)
		//uwsdoc: 	Prints an error message.
		check(logm.Define("error", log.Error))
		//uwsdoc: log.warn(format, message)
		//uwsdoc: 	Prints a warning message.
		check(logm.Define("warn", log.Warn))
		//uwsdoc: log.print(format, message)
		//uwsdoc: 	Prints a log message. Not printed if log is set as quiet or off.
		check(logm.Define("print", log.Print))
	}
	return e
}
