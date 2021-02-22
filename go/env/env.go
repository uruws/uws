// Copyright (c) Jeremías Casteglione <jeremias.tincan@gmail.com>
// See LICENSE file.

// Package env implements a config manager unsing files and env vars.
package env

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v3"
)

var prefix string;
var localPrefix string;

func parseFile(fn string) error {
	blob, err := ioutil.ReadFile(fn)
	if err != nil {
		return err
	}
	var e map[string]string
	yaml.Unmarshal(blob, &e)
	for k, v := range e {
		fmt.Printf("%s: %s\n", k, v)
	}
	return nil
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
	loadFile("override")
}

func init() {
	prefix = filepath.Clean(os.Getenv("UWS_PREFIX"))
	if prefix == "." {
		prefix = filepath.FromSlash("/uws")
	}
	localPrefix = filepath.Clean(os.Getenv("UWS_LOCAL_PREFIX"))
	if localPrefix == "." {
		localPrefix = filepath.FromSlash("/uws/local")
	}
	loadEnv()
}

// Main prints current env to stdout.
func Main(envFile string) {
	println("hello world!")
	envFile = filepath.Clean(envFile)
	if envFile != "." {
		if err := parseFile(envFile); err != nil {
			log.Fatal(err)
		}
	}
}
