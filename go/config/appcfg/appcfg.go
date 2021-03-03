// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package appcfg implements an app config manager.
package appcfg

import (
	"path/filepath"

	"uws/config"
	"uws/env"
)

type Config struct {
	*config.UserConfig
}

// New creates a new app Config instance.
func New() *Config {
	dir := env.GetFilepath("CONFIGDIR")
	if dir == "." {
		dir = filepath.FromSlash("/uws/etc")
	}
	c := config.NewUserConfig()
	c.SetConfigDir(dir)
	return &Config{c}
}
