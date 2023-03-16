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
	IsFalse(t, f.Errors, "f.Errros")
	IsEqual(t, f.Input, "-", "f.Input")
	IsFalse(t, f.Raw, "f.Raw")
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
	f.Raw = true
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
	reCheck(t, fh, reJsonLog, 51)
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
// Entry
//

func TestEntry(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	e := newEntry(f, "testing")
	IsTrue(t, e.Check(), "e.Check()")
	IsEqual(t, e.Container, "testing", "e.Container")
	IsEqual(t, e.Status, "0", "e.Status")
	IsEqual(t, e.TimeLocal, " +0000", "e.TimeLocal")
	IsTrue(t, e.Print(), "e.Print()")
}

func TestEntryCheckError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	e := newEntry(f, "testing")
	e.Status = "NOT_A_NUMBER"
	IsFalse(t, e.Check(), "e.Check()")
	IsFalse(t, e.Print(), "e.Print()")
}

func TestEntryPrint(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	e := newEntry(f, "testing")
	e.Status = "100"
	IsTrue(t, e.Check(), "e.Check() 100")
	IsTrue(t, e.Print(), "e.Print() 100")
	e.Status = "200"
	IsTrue(t, e.Check(), "e.Check() 200")
	IsTrue(t, e.Print(), "e.Print() 200")
	e.Status = "300"
	IsTrue(t, e.Check(), "e.Check() 300")
	IsTrue(t, e.Print(), "e.Print() 300")
	e.Status = "400"
	IsTrue(t, e.Check(), "e.Check() 400")
	IsTrue(t, e.Print(), "e.Print() 400")
	e.Status = "500"
	IsTrue(t, e.Check(), "e.Check() 500")
	IsTrue(t, e.Print(), "e.Print() 500")
}

func TestEntryPrintErrors(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	f.Errors = true
	e := newEntry(f, "testing")
	e.Status = "100"
	IsTrue(t, e.Check(), "e.Check() 100")
	IsFalse(t, e.Print(), "e.Print() 100")
	e.Status = "200"
	IsTrue(t, e.Check(), "e.Check() 200")
	IsFalse(t, e.Print(), "e.Print() 200")
	e.Status = "300"
	IsTrue(t, e.Check(), "e.Check() 300")
	IsFalse(t, e.Print(), "e.Print() 300")
	e.Status = "400"
	IsTrue(t, e.Check(), "e.Check() 400")
	IsTrue(t, e.Print(), "e.Print() 400")
	e.Status = "500"
	IsTrue(t, e.Check(), "e.Check() 500")
	IsTrue(t, e.Print(), "e.Print() 500")
}

//
// jsonParse
//

func TestMainJsonParse(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
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
