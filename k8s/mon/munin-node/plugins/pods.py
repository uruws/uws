#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon
import mon_kube

import pods_info
import pods_condition
import pods_container
import pods_state
import pods_top

_mods = {
	'info': dict(
		pods_info = pods_info,
		pods_condition = pods_condition,
		pods_container = pods_container,
		pods_state = pods_state,
	),
	'top': dict(
		pods_top = pods_top,
	),
}

def main():
	st = 0
	args = (
		('pods', 'info'),
		('top_pods', 'top'),
	)
	for a in args:
		mon.dbg('pods:', a[0], a[1])
		rc = _kube(a[0], a[1])
		if rc != 0:
			mon.dbg(a[0], a[1], 'failed:', rc)
			st = rc
	return st

def _kube(cmd, mods): # pragma no cover
	return mon_kube.main(sys.argv[1:], cmd, _mods[mods])

if __name__ == '__main__': # pragma no cover
	sys.exit(main())
