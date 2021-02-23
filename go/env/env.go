// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package env implements a config manager unsing files and env vars.
package env

import (
	"io/ioutil"
	"os"
	"path"
	"path/filepath"
	"strings"
	"sync"

	"gopkg.in/yaml.v3"
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
	emx.Lock()
	defer emx.Unlock()
	return yaml.Unmarshal(blob, &e)
}

func loadFile(fn string) {
	fn = filepath.Clean(filepath.FromSlash(fn))
	if fn != "." {
		fn = filepath.Join(prefix, "etc", "env", fn)
		localFn := filepath.Join(localPrefix, "etc", "env", fn)
		parseFile(fn)
		parseFile(localFn)
	}
}

func loadEnv() {
	name := path.Clean(strings.TrimSpace(os.Getenv("UWSENV")))
	loadFile("default")
	if name != "." {
		loadFile(name)
	}
	loadVars()
	loadFile("override")
}

var validVars map[string]bool = map[string]bool{
	"UWS_PREFIX": true,
	"UWS_LOCAL_PREFIX": true,
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

// Get returns the value of keyName, it returns an empty string if not set.
func Get(keyName string) string {
	emx.Lock()
	defer emx.Unlock()
	if v, ok := e[keyName]; ok {
		return v
	}
	return os.Getenv("UWS_" + keyName)
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
