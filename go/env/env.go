// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package env implements a config manager unsing files and env vars.
package env

import (
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"strings"
	"sync"

	"gopkg.in/yaml.v3"

	"uws/log"
)

var prefix string
var localPrefix string
var e map[string]string
var emx *sync.Mutex

func parseFile(fn string) error {
	blob, err := ioutil.ReadFile(fn)
	if err != nil {
		return err
	}
	return yaml.Unmarshal(blob, &e)
}

func loadFile(name string, reportError bool) error {
	n := filepath.Clean(filepath.FromSlash(name))
	if n != "." {
		var found bool = false
		fn := filepath.Join(prefix, "etc", "env", n)
		localFn := filepath.Join(localPrefix, "etc", "env", n)
		for _, fn := range []string{fn, localFn} {
			if err := parseFile(fn); err != nil {
				if reportError {
					log.Debug("%v", err)
				}
			} else {
				found = true
				if reportError {
					log.Debug("%s: env loaded", fn)
				}
			}
		}
		if reportError && !found {
			return fmt.Errorf("%s: env not found", name)
		}
	}
	return nil
}

func loadEnv() {
	name := path.Clean(strings.TrimSpace(os.Getenv("UWSENV")))
	loadFile("default", false)
	if name != "." {
		loadFile(name, false)
	}
	loadVars()
	loadFile("override", false)
}

var validVars map[string]bool = map[string]bool{
	"UWS_PREFIX": true,
	"UWS_LOCAL_PREFIX": true,
	"UWS_LOG": true,
}

func loadVars() {
	for _, s := range os.Environ() {
		if strings.HasPrefix(s, "UWS_") {
			n := strings.SplitN(s, "=", 2)[0]
			n = strings.TrimSpace(strings.Replace(n, "UWS_", "", 1))
			if n != "" {
				k := "UWS_" + n
				if validVars[k] {
					e[n] = os.Getenv(k)
				}
			}
		}
	}
}

func init() {
	e = make(map[string]string)
	emx = new(sync.Mutex)
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

func get(keyName string) string {
	if v, ok := os.LookupEnv("UWS_" + keyName); ok {
		return v
	}
	return e[keyName]
}

func expand(v string) string {
	return os.Expand(v, get)
}

// Get returns the value of keyName, it returns an empty string if not set.
func Get(keyName string) string {
	emx.Lock()
	defer emx.Unlock()
	return expand(get(keyName))
}

// List lists env keys.
func List() []string {
	emx.Lock()
	defer emx.Unlock()
	l := make([]string, 0)
	for k := range e {
		l = append(l, k)
	}
	return l
}

// Load searchs for envName file and loads it to current env.
func Load(envName ...string) error {
	emx.Lock()
	defer emx.Unlock()
	n := path.Join(envName...)
	return loadFile(n, true)
}
