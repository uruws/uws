// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package config implements a config files manager.
package config

import (
	"os"
	"path/filepath"
)

type UserConfig struct {
	*Config
	dir string
}

// NewUserConfig creates a new UserConfig instance.
func NewUserConfig() *UserConfig {
	dir, err := os.UserConfigDir()
	if err != nil {
		dir, err = os.UserHomeDir()
		if err != nil {
			dir = filepath.FromSlash("/homeless/.uws/config")
		} else {
			dir = filepath.Join(dir, ".uws", "config")
		}
	} else {
		dir = filepath.Join(dir, "uws")
	}
	return &UserConfig{Config: New()}
}

// Load searches for relname in user's config dir and loads it.
func (c *UserConfig) Load(relname ...string) error {
	n := filepath.Join(relname...)
	return parseFile(c.Config, n, true)
}

// SetConfigDir sets base user config dir.
func (c *UserConfig) SetConfigDir(dirname ...string) {
	c.dir = filepath.Join(dirname...)
}
