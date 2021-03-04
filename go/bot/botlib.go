// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package bot

import (
	"net/http"

	"uws/log"
)

func libModules(b *Bot) {
	httpModule(b)
}

func httpModule(b *Bot) {
	if m, err := b.env.Env.NewModule("http"); err != nil {
		log.Fatal("http module: %s", err)
	} else {
		// 2xx
		check(m.Define("status_ok", http.StatusOK))
		// 3xx
		check(m.Define("status_moved_permanently", http.StatusMovedPermanently))
		check(m.Define("status_found", http.StatusFound))
		check(m.Define("status_see_other", http.StatusSeeOther))
		check(m.Define("status_not_modified", http.StatusNotModified))
		check(m.Define("status_temporary_redirect", http.StatusTemporaryRedirect))
		check(m.Define("status_permanent_redirect", http.StatusPermanentRedirect))
		// 4xx
		check(m.Define("status_bad_request", http.StatusBadRequest))
		check(m.Define("status_unauthorized", http.StatusUnauthorized))
		check(m.Define("status_forbidden", http.StatusForbidden))
		check(m.Define("status_not_found", http.StatusNotFound))
		check(m.Define("status_method_not_allowed", http.StatusMethodNotAllowed))
		check(m.Define("status_request_timeout", http.StatusRequestTimeout))
		// 5xx
		check(m.Define("status_internal_server_error", http.StatusInternalServerError))
		check(m.Define("status_not_implemented", http.StatusNotImplemented))
		check(m.Define("status_bad_gateway", http.StatusBadGateway))
		check(m.Define("status_gateway_timeout", http.StatusGatewayTimeout))
	}
}
