// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package log implements a logger.
package log

import (
	"errors"
	"fmt"
	"io/ioutil"
	golog "log"
	"os"
	"sync"
)

var (
	l           *golog.Logger
	lmx         *sync.Mutex
	cdepth      int
	debugEnable bool
	verbose     bool
)

func init() {
	l = golog.New(ioutil.Discard, "", golog.Ldate|golog.Ltime)
	lmx = new(sync.Mutex)
	cdepth = 2
}

// Init initializes the logger.
func Init(name string) {
	lmx.Lock()
	defer lmx.Unlock()
	if name == "" {
		name = os.Args[0]
	}
	l.SetOutput(os.Stderr)
	lvl := os.Getenv("UWS_LOG")
	verbose = true
	if lvl == "debug" {
		debugEnable = true
		l.SetFlags(golog.Lmicroseconds | golog.Llongfile)
		l.SetPrefix(fmt.Sprintf("[%d] ", os.Getpid()))
	} else {
		l.SetFlags(golog.Lmsgprefix | golog.Ldate | golog.Lmicroseconds)
		l.SetPrefix(fmt.Sprintf("%s[%d]: ", name, os.Getpid()))
	}
	if lvl == "quiet" || lvl == "off" {
		verbose = false
	}
}

// SetPrefix sets log messages prefix. Current proccess ID is always added too.
func SetPrefix(p string) {
	lmx.Lock()
	defer lmx.Unlock()
	l.SetPrefix(fmt.Sprintf("%s[%d] ", p, os.Getpid()))
}

// Fatal prints an error message and exits with error status.
func Fatal(f string, v ...interface{}) {
	l.Output(cdepth, fmt.Sprintf("[FATAL] %s", fmt.Sprintf(f, v...)))
	os.Exit(1)
}

// Debug prints a debug message.
func Debug(f string, v ...interface{}) {
	if debugEnable {
		l.Output(cdepth, fmt.Sprintf(f, v...))
	}
}

// Error prints an error message.
func Error(f string, v ...interface{}) {
	l.Output(cdepth, fmt.Sprintf("[ERROR] %s", fmt.Sprintf(f, v...)))
}

// Warn prints a warning message.
func Warn(f string, v ...interface{}) {
	l.Output(cdepth, fmt.Sprintf("[WARNING] %s", fmt.Sprintf(f, v...)))
}

// Print prints a message.
func Print(f string, v ...interface{}) {
	if verbose {
		l.Output(cdepth, fmt.Sprintf(f, v...))
	}
}

// NewError creates a new error object, prints its message and returns it.
// Useful for situations like: return log.NewError("custom message")
func NewError(f string, v ...interface{}) error {
	err := errors.New(fmt.Sprintf(f, v...))
	l.Output(cdepth, fmt.Sprintf("[ERROR] %s", err))
	return err
}
