// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package api

import "fmt"

const (
	VMAJOR  int    = 0
	VMINOR  int    = 0
	VPATCH  int    = 0
	RELEASE string = "220419"
)

func Version() string {
	v := fmt.Sprintf("%d.%d", VMAJOR, VMINOR)
	if VPATCH > 0 {
		v = fmt.Sprintf("%s.%d", v, VPATCH)
	}
	v = fmt.Sprintf("%s-%s", v, RELEASE)
	return v
}
