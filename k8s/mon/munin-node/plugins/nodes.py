#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_kube as kube

import nodes_info

_mods = {
	'info': dict(
		nodes_info = nodes_info,
	),
}

def main():
	st = 0
	rc = _kube('nodes', 'info')
	if rc != 0:
		st = rc
	return st

def _kube(cmd, mods_name): # pragma no cover
	return kube.main(sys.argv[1:], cmd, _mods[mods_name])

if __name__ == '__main__': # pragma no cover
	sys.exit(main())
