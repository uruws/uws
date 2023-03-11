// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ngxlogs

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

func TestFlags(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	IsEqual(t, f.Input, "-", "f.Input")
	IsEqual(t, f.Format, "default", "f.Format")
}

func TestMain(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	Main(f)
}
