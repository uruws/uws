// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"encoding/json"
	"io/ioutil"
	"net/http"

	"uws/log"
)

type Response struct {
	r    *http.Response
	body []byte
}

func newResponse(r *http.Response) *Response {
	return &Response{r, nil}
}

func (r *Response) readBody() []byte {
	if r.body == nil {
		defer r.r.Body.Close()
		blob, err := ioutil.ReadAll(r.r.Body)
		if err != nil {
			log.Error("read response body: %s", err)
			return nil
		}
		r.body = blob
	}
	return r.body
}

func responseModule(b *Bot) {
	//uwsdoc: -----
	//uwsdoc: response module:
	if m, err := b.env.Env.NewModule("response"); err != nil {
		log.Fatal("response module: %s", err)
	} else {
		//uwsdoc: response.json_map(resp) -> (map[string]interface{}, error)
		//uwsdoc: 	Parses response body as a json map object.
		check(m.Define("json_map", respJSONMap))
	}
}

func respJSONMap(r *Response) (map[string]interface{}, error) {
	m := make(map[string]interface{})
	body := r.readBody()
	if body == nil {
		return nil, log.NewError("empty response body")
	}
	if err := json.Unmarshal(body, &m); err != nil {
		return nil, log.DebugError(err)
	}
	return m, nil
}
