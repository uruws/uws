// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

package bot

import (
	"uws/log"
)

// BotSession manages a logged in http session.
type BotSession struct {
}

// Login returns a session logged in to uri. Any error is reported as log.Fatal.
func Login(uri string) *BotSession {
	log.Debug("session login %s", uri)
	return &BotSession{}
}

// Logout ends the current session. Any error is reported as log.Fatal.
func (s *BotSession) Logout(uri string) {
	log.Debug("session logout %s", uri)
}
