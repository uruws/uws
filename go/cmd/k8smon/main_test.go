// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package main

import (
	"testing"

	"uws/testing/mock"

	. "uws/testing/check"
)

func TestMain(t *testing.T) {
	out := mock.Logger()
	defer mock.LoggerReset()
	cluster = ""
	Panics(t, main, "main")
	Match(t, "\\[FATAL\\] UWS_CLUSTER not set", out.String(), "error log")
}
