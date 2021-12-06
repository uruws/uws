#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

import mon_kube as kube
import pods_info
import pods_condition
import pods_container

if __name__ == '__main__': # pragma no cover
	mods = dict(
		pods_info = pods_info,
		pods_condition = pods_condition,
		pods_container = pods_container,
	)
	sys.exit(kube.main("pods", mods))
