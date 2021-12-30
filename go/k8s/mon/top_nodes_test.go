// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	//~ "uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupTopNodesCmd string
)

func init() {
	bupTopNodesCmd = topNodesCmd
}

func TestTopNodesCmd(t *testing.T) {
	IsEqual(t, topNodesCmd, "top nodes --no-headers", "top nodes cmd")
}

var topNodesInfo string = `ip-192-168-14-101.ec2.internal   62m   3%    731Mi   10%
ip-192-168-6-89.ec2.internal     63m   3%    887Mi   12%
ip-192-168-60-59.ec2.internal    73m   3%    891Mi   12%
`

func TestParseTopNodes(t *testing.T) {
	out := []byte(topNodesInfo)
	tn := new(topNodes)
	err := parseTopNodes(tn, out)
	IsNil(t, err, "parse error")
	IsEqual(t, tn.Count, uint(3), "top nodes count")
}
