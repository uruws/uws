// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

// Package env implements a config manager unsing files and env vars.
package env

import (
	"os"
	"path"
	"path/filepath"
	"strings"

	"uws/config"
	"uws/log"
)

var (
	prefix string
	localPrefix string
	e *config.Config
)

func loadFile(name string, reportError bool) error {
	n := filepath.Clean(filepath.FromSlash(name))
	if n != "." {
		var found bool = false
		fn := filepath.Join(prefix, "etc", "env", n)
		localFn := filepath.Join(localPrefix, "etc", "env", n)
		for _, fn := range []string{fn, localFn} {
			if err := e.Load(fn); err != nil {
				if reportError {
					log.Debug("env load: %s", err)
				}
			} else {
				if reportError {
					found = true
				}
				log.Debug("env loaded: %s", fn)
			}
		}
		if reportError && !found {
			return log.NewError("could not load env: %s", name)
		}
	}
	return nil
}

func loadVars(name string) {
	max := 128 // load up to max vars, just in case.
	i := 0
	for _, s := range os.Environ() {
		if i >= max {
			log.Init("")
			log.Fatal("max load of vars limit reached: %d", i)
		}
		if strings.HasPrefix(s, "UWS_") {
			n := strings.SplitN(s, "=", 2)[0]
			n = strings.TrimSpace(strings.Replace(n, "UWS_", "", 1))
			if n != "" {
				k := "UWS_" + n
				e.Set(n, os.Getenv(k))
				i += 1
			}
		}
	}
	e.Set("ENV", name)
}

func loadEnv() {
	name := path.Clean(strings.TrimSpace(os.Getenv("UWSENV")))
	loadFile("default", false)
	if name != "." {
		loadFile(name, true)
	}
	loadVars(name)
	loadFile("override", false)
}

func init() {
	e = config.New()
	prefix = filepath.Clean(os.Getenv("UWS_PREFIX"))
	if prefix == "." {
		prefix = filepath.FromSlash("/uws")
	}
	localPrefix = filepath.Clean(os.Getenv("UWS_LOCAL_PREFIX"))
	if localPrefix == "." {
		localPrefix = filepath.FromSlash("/uws/local")
	}
	os.Setenv("UWS_PREFIX", prefix)
	os.Setenv("UWS_LOCAL_PREFIX", localPrefix)
	loadEnv()
}

// Load searchs for envName file and loads it to current env.
func Load(envName ...string) error {
	n := path.Join(envName...)
	return loadFile(n, true)
}

// List lists env keys.
func List() []string {
	return e.List()
}

// Set sets env key/value. No checks are done.
func Set(key, value string) {
	e.Set(key, value)
}

// Get returns the value of keyName, it returns an empty string if not set.
func Get(keyName string) string {
	if v, ok := os.LookupEnv("UWS_" + keyName); ok {
		return v
	}
	return e.Get(keyName)
}

// GetFilepath returns a Clean'ed and Abs if possible filepath value, if not empty.
func GetFilepath(keyName string) string {
	if p, ok := os.LookupEnv("UWS_" + keyName); ok {
		p = filepath.Clean(p)
		if abs, err := filepath.Abs(p); err != nil {
			p = abs
		}
		return p
	}
	return e.GetFilepath(keyName)
}
