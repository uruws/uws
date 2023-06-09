#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import PIPE
from subprocess import Popen

import mon

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'

#
# configs and reports
#

def _print(*args):
	print(*args)

def _config(sts):
	mon.dbg('mnppl config')
	cluster = mon.cluster()
	_print('multigraph mnppl')
	_print(f"graph_title {cluster} mnppl")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category deploy')
	_print('graph_vlabel number')
	_print('graph_printf %3.0lf')
	_print('graph_scale yes')
	# FIXME: loop sts keys
	_print('a_total.label total')
	_print('a_total.colour COLOUR0')
	_print('a_total.draw AREA')
	_print('a_total.min 0')

def _report(sts):
	mon.dbg('mnppl report')
	_print('multigraph mnppl')
	# FIXME: loop sts keys
	_print('a_total.value', sts.get('total', 'U'))

#
# run parallel
#

def _listPlugins(bindir: str) -> list[str]:
	l = []
	for fn in os.listdir(bindir):
		fn = fn.strip()
		if fn.endswith(plugins_suffix):
			l.append(fn)
	return sorted(l)

def _newProc(cmd: list[str]) -> Popen:
	return Popen(cmd, text = True, stdout = PIPE, stderr = PIPE)

def _pprint(p: Popen):
	if p.returncode != 0:
		print('[ERROR]', p.args, 'failed:', p.returncode, file = sys.stderr)
	if p.stderr is not None:
		sys.stderr.write(p.stderr.read())
		sys.stderr.flush()
	if p.stdout is not None:
		sys.stdout.write(p.stdout.read())
		sys.stdout.flush()

def _run(bindir: str, action: str) -> int:
	sts: dict[str, str] = {}
	pwait: list[Popen] = []
	for pl in _listPlugins(bindir):
		cmd = [Path(bindir, pl).as_posix()]
		if action == 'config':
			cmd.append(action)
		pwait.append(_newProc(cmd))
		sts[pl] = ''
	rc = 0
	for proc in pwait:
		st = proc.wait()
		if st != 0:
			rc = st
		_pprint(proc)
	if action == 'config':
		_config(sts)
	else:
		_report(sts)
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

	rc = 0
	if args.serial:
		for pl in _listPlugins(args.bindir):
			st = os.system(Path(args.bindir, pl))
			if st != 0:
				rc = st
	else:
		return _run(args.bindir, action)
	return rc

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
