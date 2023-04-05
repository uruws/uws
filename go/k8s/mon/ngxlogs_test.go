// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	//~ "uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupNgxlogsCmd string
)

func init() {
	bupNgxlogsCmd = ngxlogsCmd
}

func TestNgxlogsCmd(t *testing.T) {
	IsEqual(t, ngxlogsCmd, "logs -l 'app.kubernetes.io/name=proxy --max-log-requests 100 --ignore-errors=true --prefix=true --timestamps=true", "ngxlogs cmd")
}
