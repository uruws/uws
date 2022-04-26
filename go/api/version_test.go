// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package api

import (
	"fmt"
	"testing"

	. "uws/testing/check"
)

func TestVersion(t *testing.T) {
	v := fmt.Sprintf("%d.%d", VMAJOR, VMINOR)
	if VPATCH > 0 {
		v = fmt.Sprintf("%s.%d", v, VPATCH)
	}
	v = fmt.Sprintf("%s-%s", v, RELEASE)
	IsEqual(t, Version(), v, "api version")
}
