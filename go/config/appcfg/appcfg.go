// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package config

import (
	"os"
	"path/filepath"

	"uws/config"
	"uws/env"
)

type AppConfig struct {
	*config.UserConfig
}

// NewAppConfig creates a new AppConfig instance.
func NewAppConfig() *AppConfig {
	dir := env.GetFilepath("CONFIGDIR")
	if dir == "." {
		dir = filepath.FromSlash("/uws/etc")
	}
	return &AppConfig{&config.UserConfig{Config: New(), dir: dir}}
}
