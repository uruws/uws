// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mock

import (
	"bytes"

	"uws/log"
)

var loggerOut *bytes.Buffer

func init() {
	loggerOut = new(bytes.Buffer)
}

func Logger() *bytes.Buffer {
	log.Mock(loggerOut)
	return loggerOut
}

func LoggerReset() {
	log.MockReset()
	loggerOut.Reset()
}

func LoggerOutput() string {
	return loggerOut.String()
}
