#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys
sys.path.insert(0, '/uws/lib/plugins')

import main

if __name__ == '__main__':
	sys.exit(main.run(sys.argv[:]))
