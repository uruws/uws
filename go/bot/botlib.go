// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"fmt"
	"net/http"
	"net/url"

	"uws/log"
)

func libModules(b *Bot) {
	httpModule(b)
	urlModule(b)
}

func httpModule(b *Bot) {
	//uwsdoc: -----
	//uwsdoc: http module:
	if m, err := b.env.Env.NewModule("http"); err != nil {
		log.Fatal("http module: %s", err)
	} else {
		// 2xx
		//uwsdoc: http.status_ok                    = 200
		check(m.Define("status_ok", http.StatusOK))
		// 3xx
		//uwsdoc: http.status_moved_permanently     = 301
		check(m.Define("status_moved_permanently", http.StatusMovedPermanently))
		//uwsdoc: http.status_found                 = 302
		check(m.Define("status_found", http.StatusFound))
		//uwsdoc: http.status_see_other             = 303
		check(m.Define("status_see_other", http.StatusSeeOther))
		//uwsdoc: http.status_not_modified          = 304
		check(m.Define("status_not_modified", http.StatusNotModified))
		//uwsdoc: http.status_temporary_redirect    = 307
		check(m.Define("status_temporary_redirect", http.StatusTemporaryRedirect))
		//uwsdoc: http.status_permanent_redirect    = 308
		check(m.Define("status_permanent_redirect", http.StatusPermanentRedirect))
		// 4xx
		//uwsdoc: http.status_bad_request           = 400
		check(m.Define("status_bad_request", http.StatusBadRequest))
		//uwsdoc: http.status_unauthorized          = 401
		check(m.Define("status_unauthorized", http.StatusUnauthorized))
		//uwsdoc: http.status_forbidden             = 403
		check(m.Define("status_forbidden", http.StatusForbidden))
		//uwsdoc: http.status_not_found             = 404
		check(m.Define("status_not_found", http.StatusNotFound))
		//uwsdoc: http.status_method_not_allowed    = 405
		check(m.Define("status_method_not_allowed", http.StatusMethodNotAllowed))
		//uwsdoc: http.status_request_timeout       = 408
		check(m.Define("status_request_timeout", http.StatusRequestTimeout))
		// 5xx
		//uwsdoc: http.status_internal_server_error = 500
		check(m.Define("status_internal_server_error", http.StatusInternalServerError))
		//uwsdoc: http.status_not_implemented       = 501
		check(m.Define("status_not_implemented", http.StatusNotImplemented))
		//uwsdoc: http.status_bad_gateway           = 502
		check(m.Define("status_bad_gateway", http.StatusBadGateway))
		//uwsdoc: http.status_service_unavailable   = 503
		check(m.Define("status_bad_gateway", http.StatusServiceUnavailable))
		//uwsdoc: http.status_gateway_timeout       = 504
		check(m.Define("status_gateway_timeout", http.StatusGatewayTimeout))
	}
}

func urlModule(b *Bot) {
	//uwsdoc: -----
	//uwsdoc: url module:
	if m, err := b.env.Env.NewModule("url"); err != nil {
		log.Fatal("url module: %s", err)
	} else {
		//uwsdoc: url.parse_query(string) -> values
		//uwsdoc: 	Parse an url string and returns its values to be used as a query
		//uwsdoc: 	string or as form (url-encoded) data.
		check(m.Define("parse_query", urlParseQuery))
		//uwsdoc: url.parse_queryf(format, args...) -> values
		//uwsdoc: 	It works like url.parse_query but you can format the query
		//uwsdoc: 	string. Like in example:
		//uwsdoc: 		url.parse_queryf("id=%d&name=%s", id, name)
		check(m.Define("parse_queryf", urlParseQueryf))
	}
}

func urlParseQuery(q string) url.Values {
	v, err := url.ParseQuery(q)
	if err != nil {
		log.Fatal("url.parse_query: %s", err)
	}
	return v
}

func urlParseQueryf(format string, args ...interface{}) url.Values {
	return urlParseQuery(fmt.Sprintf(format, args...))
}
