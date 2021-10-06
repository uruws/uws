#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/opt/munin/lib')

import alerts

if __name__ == '__main__':
	sys.exit(alerts.message())
