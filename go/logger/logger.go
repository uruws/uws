// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package logger implements a log manager.
package logger

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sync"
)

type Logger struct {
	*log.Logger
}

var l *Logger
var lmx *sync.Mutex

func init() {
	l = &Logger{Logger: log.New(ioutil.Discard, "", log.Ldate | log.Ltime)}
	lmx = new(sync.Mutex)
}

func newLogger() *Logger {
	return &Logger{Logger: log.New(os.Stderr, "", log.Ldate | log.Lmsgprefix | log.Lmicroseconds)}
}

// New initializes a new Logger.
func New(name string) *Logger {
	lmx.Lock()
	defer lmx.Unlock()
	l = newLogger()
	if os.Getenv("UWS_LOG") == "debug" {
		l.SetFlags(log.Lmsgprefix | log.Lmicroseconds | log.Llongfile)
	}
	l.SetPrefix(fmt.Sprintf("%s[%d]: ", name, os.Getpid()))
	return l
}

// Get returns the current Logger instance.
func Get() *Logger {
	lmx.Lock()
	defer lmx.Unlock()
	return l
}
