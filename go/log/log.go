// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package log implements a logger.
package log

import (
	"fmt"
	"io/ioutil"
	golog "log"
	"os"
	"sync"
)

var (
	l *golog.Logger
	lmx *sync.Mutex
	cdepth int
	debugEnable bool
)

func init() {
	l = golog.New(ioutil.Discard, "", golog.Ldate | golog.Ltime)
	lmx = new(sync.Mutex)
	cdepth = 2
}

// Init initializes the logger.
func Init(name string) {
	lmx.Lock()
	defer lmx.Unlock()
	l.SetOutput(os.Stderr)
	if os.Getenv("UWS_LOG") == "debug" {
		debugEnable = true
		l.SetFlags(golog.Lmsgprefix | golog.Lmicroseconds | golog.Llongfile)
		l.SetPrefix(fmt.Sprintf("[%d] ", os.Getpid()))
	} else {
		l.SetFlags(golog.Lmsgprefix | golog.Ldate | golog.Lmicroseconds)
		l.SetPrefix(fmt.Sprintf("%s[%d]: ", name, os.Getpid()))
	}
}

// Fatal prints an error message and exits with error status.
func Fatal(f string, v ...interface{}) {
	l.Output(cdepth, fmt.Sprintf("[FATAL] %s", fmt.Sprintf(f, v...)))
	os.Exit(1)
}

// Debug prints a debug message.
func Debug(f string, v ...interface{}) {
	if debugEnable {
		l.Output(cdepth, fmt.Sprintf("[D] %s", fmt.Sprintf(f, v...)))
	}
}

// Error prints an error message.
func Error(f string, v ...interface{}) {
	l.Output(cdepth, fmt.Sprintf("[ERROR] %s", fmt.Sprintf(f, v...)))
}
