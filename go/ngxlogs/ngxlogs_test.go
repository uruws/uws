// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package ngxlogs

import (
	"bufio"
	"errors"
	"io"
	"os"
	"regexp"

	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

//
// Main
//

func TestFlags(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	IsFalse(t, f.Errors, "f.Errros")
	IsEqual(t, f.Input, "-", "f.Input")
	IsFalse(t, f.Raw, "f.Raw")
	IsTrue(t, f.Stats, "f.Stats")
}

func TestMain(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	Main(f)
}

func TestMainFileNotFound(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	f := NewFlags()
	f.Input = "/file/not/found.testing"
	fn := func() {
		Main(f)
	}
	Panics(t, fn, "Main")
}

func TestMainParseError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	var bupRawOutput func(r io.Reader) error
	bupRawOutput = rawOutput
	rawOutput = func(r io.Reader) error {
		return errors.New("testing")
	}
	defer func() {
		rawOutput = bupRawOutput
	}()
	f := NewFlags()
	f.Raw = true
	f.Input = "./testdata/json-error.logs"
	fn := func() {
		Main(f)
	}
	Panics(t, fn, "Main")
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
// Stats
//

func TestStats(t *testing.T) {
	s := newStats()
	IsEqual(t, s.NgxErrors, 0, "s.NgxErrors")
	IsEqual(t, s.NgxStarts, 0, "s.NgxStarts")
	IsEqual(t, s.Requests, 0, "s.Requests")
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
	p := jsonParse(f, fh)
	IsNil(t, p.Error, "json parse")
	IsEqual(t, p.Lines, 69, "p.Lines")
	IsEqual(t, p.Read, 57, "p.Read")
	IsEqual(t, p.LinesError, 0, "p.LinesError")
	IsEqual(t, p.Unknown, 12, "p.Unknown")
	// Stats
	IsEqual(t, p.Stats.NgxErrors, 3, "p.Stats.NgxErrors")
	IsEqual(t, p.Stats.NgxStarts, 3, "p.Stats.NgxStarts")
	IsEqual(t, p.Stats.Requests, 51, "p.Stats.Requests")
	IsEqual(t, p.Stats.OK, 43, "p.Stats.OK")
	IsEqual(t, p.Stats.Warning, 5, "p.Stats.Warning")
	IsEqual(t, p.Stats.Error, 3, "p.Stats.Error")
	IsEqual(t, p.Stats.Websocket, 0, "p.Stats.Websocket")
	// cover p.PrintStats
	IsTrue(t, p.PrintStats(), "p.PrintStats()")
}

func TestJsonParseNoStats(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	f := NewFlags()
	f.Stats = false
	p := jsonParse(f, fh)
	IsNil(t, p.Error, "json parse")
	IsFalse(t, p.PrintStats(), "p.PrintStats()")
}

func TestJsonParseError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/uwsdev-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	fh.Close()
	f := NewFlags()
	p := jsonParse(f, fh)
	NotNil(t, p.Error, "parse error")
	IsEqual(t, p.Lines, 0, "p.Lines")
	IsEqual(t, p.Read, 0, "p.Read")
	IsEqual(t, p.LinesError, 0, "p.LinesError")
	IsEqual(t, p.Unknown, 0, "p.Unknown")
}

func TestJsonParseReadError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/json-error.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	f := NewFlags()
	p := jsonParse(f, fh)
	IsNil(t, p.Error, "parse read error")
	IsEqual(t, p.Lines, 3, "p.Lines")
	IsEqual(t, p.Read, 2, "p.Read")
	IsEqual(t, p.LinesError, 1, "p.LinesError")
	IsEqual(t, p.Unknown, 0, "p.Unknown")
}

func TestJsonParseInvalid(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/json-invalid.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	defer fh.Close()
	f := NewFlags()
	p := jsonParse(f, fh)
	IsNil(t, p.Error, "parse invalid")
	IsEqual(t, p.Lines, 3, "p.Lines")
	IsEqual(t, p.Read, 1, "p.Read")
	IsEqual(t, p.LinesError, 1, "p.LinesError")
	IsEqual(t, p.Unknown, 1, "p.Unknown")
}

func TestJsonParseWebsocket(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	fh, err := os.Open("./testdata/meteor-gw.logs")
	Fatal(t, IsNil(t, err, "read logs"))
	f := NewFlags()
	p := jsonParse(f, fh)
	IsNil(t, p.Error, "parse error")
	IsEqual(t, p.Lines, 100, "p.Lines")
	IsEqual(t, p.Read, 100, "p.Read")
	IsEqual(t, p.Stats.Websocket, 2, "p.Stats.Websocket")
}
