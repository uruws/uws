#!/usr/bin/env python3
# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess
import sys

cmdpath:    str = '/usr/bin/ab'
user_agent: str = '-HUser-Agent:uwsab'

def _run(cmd):
	return subprocess.run(cmd, shell = True, stdout = sys.stdout, stderr = sys.stderr)

def main(argv: list[str] = []) -> int:
	cmd = '%s %s %s' % (cmdpath, user_agent, ' '.join(argv))
	proc = _run(cmd)
	return proc.returncode

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
