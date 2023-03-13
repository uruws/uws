// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ngxlogs

import (
	"os"

	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

func TestFlags(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	IsEqual(t, f.Input, "-", "f.Input")
	IsEqual(t, f.Format, "default", "f.Format")
}

func TestMain(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	Main(f)
}

func TestMainJsonParser(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	f.Format = "json"
	f.Input = "./testdata/uwsdev-gw.logs"
	Main(f)
}

func TestJsonParser(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	err = jsonParse(fh)
	IsNil(t, err, "json parse")
}

func TestJsonParserError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	fh.Close()
	err = jsonParse(fh)
	NotNil(t, err, "parse error")
}
