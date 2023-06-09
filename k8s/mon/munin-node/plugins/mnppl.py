#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import PIPE
from subprocess import Popen

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'

def _listPlugins(bindir: str) -> list[str]:
	l = []
	for fn in os.listdir(bindir):
		fn = fn.strip()
		if fn.endswith(plugins_suffix):
			l.append(fn)
	return sorted(l)

#
# run parallel
#

def _newProc(cmd: list[str]) -> Popen:
	return Popen(cmd, text = True, stdout = PIPE, stderr = PIPE)

def _pprint(p: Popen):
	if p.returncode != 0:
		print('[ERROR]', ' '.join(p.args), 'failed:', p.returncode, file = sys.stderr)
	if p.stderr is not None:
		sys.stderr.write(p.stderr.read())
		sys.stderr.flush()
	if p.stdout is not None:
		sys.stdout.write(p.stdout.read())
		sys.stdout.flush()

def _run(bindir: str, action: str) -> int:
	pwait: list[Popen] = []
	for pl in _listPlugins(bindir):
		cmd = [Path(bindir, pl).as_posix()]
		if action == 'config':
			cmd.append(action)
		pwait.append(_newProc(cmd))
	rc = 0
	for proc in pwait:
		st = proc.wait()
		if st != 0:
			rc = st
		_pprint(proc)
	return rc

#
# main
#

__doc__ = 'munin-node parallel plugins runner'

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-b', '--bindir', default = plugins_bindir,
		help = 'plugins bindir')
	flags.add_argument('-s', '--serial', action = 'store_true', default = False,
		help = 'no parallelism')
	flags.add_argument('action', default = 'report', nargs = '*',
		choices = ['config', 'report'],
		help = 'plugin action')

	args = flags.parse_args(argv)

	action = 'report'
	if isinstance(args.action, list):
		action = args.action[0].strip()

	bindir = Path(args.bindir)

	rc = 0
	if args.serial:
		for pl in _listPlugins(bindir):
			st = os.system(Path(bindir, pl))
			if st != 0:
				rc = st
	else:
		return _run(bindir, action)
	return rc

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
