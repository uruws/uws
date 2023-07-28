#!/usr/bin/env python3
# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess
import sys

cmdpath: str = '/usr/bin/ab'

def _run(cmd):
	return subprocess.run(cmd, shell = True, stdout = sys.stdout, stderr = sys.stderr)

def main(argv: list[str] = []) -> int:
	cmd = '%s %s' % (cmdpath, ' '.join(argv))
	proc = _run(cmd)
	return proc.returncode

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
