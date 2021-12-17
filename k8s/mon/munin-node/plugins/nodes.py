#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_kube as kube

import nodes_info

if __name__ == '__main__': # pragma no cover
	mods = dict(
		nodes_info = nodes_info,
	)
	sys.exit(kube.main(sys.argv[1:], "nodes", mods))
