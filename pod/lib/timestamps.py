#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from datetime import datetime

def _ts():
	ts = datetime.now()
	return ts.strftime('%Y%m%d %H:%M:%S')

def main(argv = []):
	while True:
		try:
			line = sys.stdin.readline().strip()
		except KeyboardInterrupt:
			break
		if line == '':
			break
		print(_ts(), line, flush = True)
	return 0

if __name__ == '__main__': # pragma no cover
	sys.stdout.reconfigure(line_buffering = False) # type: ignore
	sys.stderr.reconfigure(line_buffering = False) # type: ignore
	sys.exit(main(sys.argv[1:]))
