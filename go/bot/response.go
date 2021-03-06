// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"

	//~ "uws/log"
)

type Response struct {
	r *http.Response
	body []byte
}

func newResponse(r *http.Response) *Response {
	return &Response{r, nil}
}
