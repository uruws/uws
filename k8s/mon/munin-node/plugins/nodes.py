#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_kube as kube

import nodes_info
import nodes_taint
import nodes_top

_mods = {
	'info': dict(
		nodes_info = nodes_info,
		nodes_taint = nodes_taint,
	),
	'top': dict(
		nodes_top = nodes_top,
	),
}

def main():
	st = 0
	args = (
		('nodes', 'info'),
		('top_nodes', 'top'),
	)
	for a in args:
		rc = _kube(a[0], a[1])
		if rc != 0:
			st = rc
	return st

def _kube(cmd, mods_name): # pragma no cover
	return kube.main(sys.argv[1:], cmd, _mods[mods_name])

if __name__ == '__main__': # pragma no cover
	sys.exit(main())
