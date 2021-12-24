// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mock

import (
	"net/http"
)

func HTTPListenAndServe(addr string, h http.Handler) error {
	return nil
}
