// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package config implements a config files manager.
package config

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"gopkg.in/yaml.v3"
)

type Config struct {
	d  map[string]string
	dx *sync.Mutex
}

// New creates a new Config instance.
func New() *Config {
	return &Config{
		d: make(map[string]string),
		dx: new(sync.Mutex),
	}
}

// Open parses filename and creates a new config instance.
func Open(filename ...string) (*Config, error) {
	c := New()
	return c, c.Load(filename...)
}

// Load parses filename and loads it config.
func (c *Config) Load(filename ...string) error {
	n := filepath.Join(filename...)
	return parseFile(c, n, true)
}

// List lists config keys.
func (c *Config) List() []string {
	c.dx.Lock()
	defer c.dx.Unlock()
	l := make([]string, 0)
	for k := range c.d {
		l = append(l, k[:])
	}
	return l
}

// Set sets key/value. No checks are done.
func (c *Config) Set(key, value string) {
	c.dx.Lock()
	defer c.dx.Unlock()
	c.d[key[:]] = value[:]
}

func (c *Config) get(keyName string) string {
	return c.d[keyName]
}

func (c *Config) expand(v string) string {
	if v != "" {
		return os.Expand(v, c.get)
	}
	return ""
}

// Get returns the value of keyName, it returns an empty string if not set.
func (c *Config) Get(keyName string) string {
	c.dx.Lock()
	defer c.dx.Unlock()
	return c.expand(c.d[keyName])
}

// GetFilepath returns a Clean'ed and Abs if possible filepath value, if not empty.
func (c *Config) GetFilepath(keyName string) string {
	v := filepath.Clean(c.Get(keyName))
	if abs, err := filepath.Abs(v); err != nil {
		v = abs
	}
	return v
}

func includeFiles(c *Config, list string) error {
	for _, n := range strings.Split(list, " ") {
		if err := parseFile(c, n, false); err != nil {
			return err
		}
	}
	return nil
}

func parseFile(c *Config, fn string, incEnable bool) error {
	c.dx.Lock()
	defer c.dx.Unlock()
	blob, err := ioutil.ReadFile(fn)
	if err != nil {
		return err
	}
	p := make(map[string]string)
	if err := yaml.Unmarshal(blob, &p); err != nil {
		return err
	} else {
		for k, v := range p {
			if k == "include" && incEnable {
				if err := includeFiles(c, v); err != nil {
					return err
				}
			}
			if k != "include" {
				c.d[k[:]] = v[:]
			}
		}
	}
	return nil
}

// global config instance

var cfg *Config

func init() {
	cfg = New()
}

// Load parses filename and loads it to global config.
func Load(filename ...string) error {
	return cfg.Load(filename...)
}

// List global config.
func List() []string {
	return cfg.List()
}

// Set to global config.
func Set(key, value string) {
	cfg.Set(key, value)
}

// Get from global config.
func Get(keyName string) string {
	return cfg.Get(keyName)
}

// GetFilepath from global config.
func GetFilepath(keyName string) string {
	return cfg.GetFilepath(keyName)
}
