// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ctl

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

func TestNodegroupUpgrade(t *testing.T) {
	mockCtl()
	defer mockCtlReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	NodegroupUpgrade(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	//~ IsEqual(t, mock.HTTPResponseString(resp), `{"status":"ok","message":"testing"}`, "resp body")
}
