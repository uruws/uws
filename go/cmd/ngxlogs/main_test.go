// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package main

import (
	"testing"
	"uws/testing/mock"
)

func TestMain(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	main()
}
