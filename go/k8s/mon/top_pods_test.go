// Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
// See LICENSE file.

package mon

import (
	"testing"
	"uws/testing/mock"

	. "uws/testing/check"
)

var (
	bupTopPodsCmd string
)

func init() {
	bupTopPodsCmd = topPodsCmd
}

func TestTopPodsCmd(t *testing.T) {
	IsEqual(t, topPodsCmd, "top pods -A --no-headers", "top pods cmd")
}

var topPodsInfo string = `
cert-manager    cert-manager-66b6d6bf59-xsx76               1m    23Mi
cert-manager    cert-manager-cainjector-856d4df858-csjg7    3m    51Mi
cert-manager    cert-manager-webhook-6d866ffbc7-pq4mw       2m    14Mi
ingress-nginx   ingress-nginx-controller-59c8576d75-qbms9   3m    76Mi
kube-system     aws-node-5lmld                              4m    41Mi
kube-system     aws-node-fp6c6                              5m    41Mi
kube-system     aws-node-lnmz9                              5m    41Mi
kube-system     cluster-autoscaler-848d4b88dc-rlvx6         2m    45Mi
kube-system     coredns-7d74b564bd-9mc2d                    4m    8Mi
kube-system     coredns-7d74b564bd-l8c2t                    3m    8Mi
kube-system     kube-proxy-6zggk                            1m    13Mi
kube-system     kube-proxy-f4jnk                            2m    13Mi
kube-system     kube-proxy-q2rpf                            1m    13Mi
kube-system     metrics-server-588cd8ddb5-r6hrq             4m    20Mi
mon             k8s-54cf879cf8-6k2kv                        1m    15Mi
mon             munin-0                                     1m    55Mi
mon             munin-node-789b7d89bf-r97hf                 1m    11Mi
`

func TestParseTopPods(t *testing.T) {
	out := []byte(topPodsInfo)
	l := newTopPodsList()
	parseTopPods(l, out)
	IsEqual(t, len(l.Items), 17, "items number")
	IsEqual(t, l.Items[15].Namespace, "mon", "item namespace")
	IsEqual(t, l.Items[15].Name, "munin-0", "item name")
	IsEqual(t, l.Items[15].CPU, uint64(1), "item cpu")
	IsEqual(t, l.Items[15].Mem, uint64(55), "item mem")
}

func TestTopPodsCommandError(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	TopPods(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 500, "resp status code")
	IsEqual(t, mock.HTTPResponseString(resp),
		"error: fork/exec /usr/local/bin/uwskube: no such file or directory",
		"resp body")
}

func TestTopPods(t *testing.T) {
	mock.Logger()
	defer mock.LoggerReset()
	kubecmd = develKubecmd
	topPodsCmd = "test_top_pods"
	defer func() {
		kubecmd = bupKubecmd
		topPodsCmd = bupTopPodsCmd
	}()
	w := mock.HTTPResponse()
	r := mock.HTTPRequest()
	TopPods(w, r)
	resp := w.Result()
	IsEqual(t, resp.StatusCode, 200, "resp status code")
	IsEqual(t, resp.Header.Get("content-type"), "application/json", "resp content type")
	IsEqual(t, len(mock.HTTPResponseString(resp)), 2052, "resp body size")
}
