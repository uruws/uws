// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

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

var topNodesInfo string = `
ip-192-168-14-101.ec2.internal   62m   3%    731Mi   10%
ip-192-168-6-89.ec2.internal     63m   3%    887Mi   12%
ip-192-168-60-59.ec2.internal    73m   3%    891Mi   12%
`

func TestParseTopNodes(t *testing.T) {
	out := []byte(topNodesInfo)
	tn := new(topNodes)
	parseTopNodes(tn, out)
	IsEqual(t, tn.Count, uint(3), "top nodes count")
	IsEqual(t, tn.CPU, uint64(198), "top nodes cpu")
	IsEqual(t, tn.CPUP, uint(9), "top nodes cpu percentage")
	IsEqual(t, tn.Mem, uint64(2509), "top nodes mem")
	IsEqual(t, tn.MemP, uint(34), "top nodes mem percentage")
}

func TestTopNodesCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	TopNodes(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestTopNodes(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	topNodesCmd = "test_top_nodes"
	defer func() {
		kubecmd = bupKubecmd
		topNodesCmd = bupTopNodesCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	TopNodes(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
	tn := `{
  "count": 3,
  "cpu": 198,
  "cpu_min": 62,
  "cpu_max": 73,
  "cpup": 9,
  "cpup_min": 3,
  "cpup_max": 3,
  "mem": 2509,
  "mem_min": 731,
  "mem_max": 891,
  "memp": 34,
  "memp_min": 10,
  "memp_max": 12
}`
	IsEqual(t, mock.HTTPResponseString(resp), tn, "resp body")
}
