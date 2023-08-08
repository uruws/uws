#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon

MNPL = os.getenv('MNPL', '/uws/lib/plugins')
sys.path.insert(0, MNPL)

import mnpl

def _host() -> mnpl.HostConfig:
	return mnpl.HostConfig(
		name = 'ops',
		host = 'ops',
	)

def _cfg() -> mnpl.Config:
	cluster = mon.cleanfn(mon.cluster())
	return mnpl.Config(
		path = f"/munin/uws.t.o/cluster.uws.t.o/k8s_{cluster}__k8smon___ping_400_no_auth-day.png",
		category = 'munin',
		title = 'munin crosscheck',
	)

def main(argv: list[str]):
	h = _host()
	cfg = _cfg()
	try:
		action = argv[0]
	except IndexError:
		action = 'report'
	if action == 'config':
		return mnpl.config_host(h, cfg)
	return mnpl.report_host(h, cfg)

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
