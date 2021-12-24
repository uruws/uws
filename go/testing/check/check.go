// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

/*
Package check implements utilities to be used for asserting testing results.

Each function is a condition that must succeed, otherwise the test fails.

If a condition fails, execution of the test continues unless it's marked as
Fatal. See the examples.
*/
package check

import (
	"regexp"
	"testing"
)

// Fatal calls t.FailNow() if ok condition is false.
//
// So test execution is aborted, otherwise the test is marked as failed but
// execution continues.
func Fatal(t *testing.T, ok bool) bool {
	if !ok {
		t.FailNow()
	}
	return true
}

// IsNil fails if got param is not nil.
func IsNil(t *testing.T, got interface{}, errmsg string) bool {
	t.Helper()
	if got != nil {
		t.Errorf("%s is not nil: (%T)%v", errmsg, got, got)
		return false
	}
	return true
}

// NotNil fails if got param is not nil.
func NotNil(t *testing.T, got interface{}, errmsg string) bool {
	t.Helper()
	if got == nil {
		t.Errorf("%s is nil: (%T)%v", errmsg, got, got)
		return false
	}
	return true
}

// IsTrue fails if got param is not true.
func IsTrue(t *testing.T, got bool, errmsg string) bool {
	t.Helper()
	if !got {
		t.Errorf("%s: is %v", errmsg, got)
		return false
	}
	return true
}

// IsFalse fails if got param is not false.
func IsFalse(t *testing.T, got bool, errmsg string) bool {
	t.Helper()
	if got {
		t.Errorf("%s: is %v", errmsg, got)
		return false
	}
	return true
}

// IsEqual fails if got != expect.
func IsEqual(t *testing.T, got, expect interface{}, errmsg string) bool {
	t.Helper()
	if got != expect {
		t.Errorf("%s: '(%T)%v' != '(%T)%v'", errmsg, got, got, expect, expect)
		return false
	}
	return true
}

// NotEqual fails if got == expect.
func NotEqual(t *testing.T, got, expect interface{}, errmsg string) bool {
	t.Helper()
	if got == expect {
		t.Errorf("%s: '(%T)%v' == '(%T)%v'", errmsg, got, got, expect, expect)
		return false
	}
	return true
}

// Match fails if string s does not match pat regexp.
func Match(t *testing.T, pat, s, errmsg string) bool {
	t.Helper()
	m, err := regexp.MatchString(pat, s)
	if err != nil {
		t.Fatalf("ERROR %s: %s", errmsg, err)
		return false
	}
	if !m {
		t.Errorf("%s: '%s' mismatch '%s'", errmsg, pat, s)
		return false
	}
	return true
}

// NotMatch fails if string s matches pat regexp.
func NotMatch(t *testing.T, pat, s, errmsg string) bool {
	t.Helper()
	m, err := regexp.MatchString(pat, s)
	if err != nil {
		t.Fatalf("ERROR %s: %s", errmsg, err)
		return false
	}
	if m {
		t.Errorf("%s: '%s' match '%s'", errmsg, pat, s)
		return false
	}
	return true
}

// Panics checks if the given func panics.
func Panics(t *testing.T, f func(), errmsg string) bool {
	t.Helper()
	v := false
	defer func() {
		if r := recover(); r != nil {
			v = true
		}
	}()
	f()
	if !v {
		t.Fatalf("%s: did not panic", errmsg)
	}
	return v
}
