// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ngxlogs

import (
	"bufio"
	"io"
	"os"
	"regexp"

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

//
// rawOutput
//

func TestMainRawOutput(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	f.Format = "raw"
	f.Input = "./testdata/uwsdev-gw.logs"
	Main(f)
}

func TestRawOutput(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	err = rawOutput(fh)
	IsNil(t, err, "json parse")
}

func TestRawOutputError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	fh.Close()
	err = rawOutput(fh)
	NotNil(t, err, "parse error")
}

//
// regexp
//

func reCheck(t *testing.T, fh io.Reader, re *regexp.Regexp, count int) {
	t.Helper()
	got := 0
	x := bufio.NewScanner(fh)
	for x.Scan() {
		if re.Match(x.Bytes()) {
			got += 1
		}
	}
	Fatal(t, IsNil(t, x.Err(), "scanner error"))
	IsEqual(t, got, count, "regexp count")
}

func TestReJsonLog(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	reCheck(t, fh, reJsonLog, 50)
}

func TestReErrorLog(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	reCheck(t, fh, reErrorLog, 3)
}

func TestReStartLog(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	reCheck(t, fh, reStartLog, 3)
}

//
// jsonParse
//

func TestMainJsonParse(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	f.Format = "json"
	f.Input = "./testdata/uwsdev-gw.logs"
	Main(f)
}

func TestJsonParse(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	f := NewFlags()
	err = jsonParse(f, fh)
	IsNil(t, err, "json parse")
}

func TestJsonParseError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	fh.Close()
	f := NewFlags()
	err = jsonParse(f, fh)
	NotNil(t, err, "parse error")
}
