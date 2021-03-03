// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package config

import (
	"os"
	"path/filepath"

	"uws/env"
)

type AppConfig struct {
	*UserConfig
}

// NewAppConfig creates a new AppConfig instance.
func NewAppConfig() *AppConfig {
	dir := env.GetFilepath("CONFIGDIR")
	if dir == "." {
		dir = filepath.FromSlash("/uws/etc")
	}
	return &AppConfig{&UserConfig{Config: New(), dir: dir}}
}
