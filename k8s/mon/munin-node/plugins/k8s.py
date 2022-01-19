#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

# load lib

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_metrics as metrics

# load env

_k8s_metrics = 'http://k8s.mon.svc.cluster.local:2800/kube/k8s_metrics'
METRICS_URL = os.getenv('K8S_METRICS_URL', _k8s_metrics)

# load modules

import k8s_cpu
import k8s_etcd
import k8s_mem

if __name__ == '__main__': # pragma no cover
	mods = dict()
	mods = dict(
		k8s_cpu = k8s_cpu,
		k8s_etcd = k8s_etcd,
		k8s_mem = k8s_mem,
	)
	sys.exit(metrics.main(sys.argv[1:], METRICS_URL, mods))
