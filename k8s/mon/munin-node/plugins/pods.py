#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_kube

import pods_info
import pods_condition
import pods_container

_mods = {
	'info': dict(
		pods_info = pods_info,
		pods_condition = pods_condition,
		pods_container = pods_container,
	),
}

def main():
	st = 0
	args = (
		('pods', 'info'),
	)
	for a in args:
		rc = _kube(a[0], _mods[a[1]])
		if rc != 0:
			st = rc
	return st

def _kube(cmd, mods): # pragma no cover
	return mon_kube.main(sys.argv[1:], cmd, mods)

if __name__ == '__main__': # pragma no cover
	sys.exit(main)
