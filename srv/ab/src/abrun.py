#!/usr/bin/env python3
# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess
import sys

from time import asctime
from time import gmtime

cmdpath:    str = '/usr/bin/ab'
user_agent: str = '-HUser-Agent:uwsab'

_outfh = sys.stdout

def _datetime(tag: str):
	print('%s:' % tag, asctime(gmtime()), file = _outfh)

def _run(cmd):
	return subprocess.run(cmd, shell = True, stdout = sys.stdout, stderr = sys.stderr)

def main(argv: list[str] = []) -> int:
	cmd = '%s %s %s' % (cmdpath, user_agent, ' '.join(argv))
	_datetime('Start')
	proc = _run(cmd)
	_datetime('End')
	return proc.returncode

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
