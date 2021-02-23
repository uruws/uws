// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package logger implements a log manager.
package logger

import (
	"fmt"
	"log"
	"os"
)

type Logger struct {
	*log.Logger
}

func newLogger() *Logger {
	return &Logger{Logger: log.New(os.Stderr, "", log.Ldate | log.Lmsgprefix | log.Lmicroseconds)}
}

var l *Logger

func init() {
	l = newLogger()
}

// New initializes a new Logger.
func New(name string) *Logger {
	if os.Getenv("UWS_LOG") == "debug" {
		l.SetFlags(log.Lmsgprefix | log.Lmicroseconds | log.Llongfile)
	}
	l.SetPrefix(fmt.Sprintf("%s[%d]: ", name, os.Getpid()))
	return l
}

// Get returns the current Logger instance.
func Get() *Logger {
	return l
}
