#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import PIPE
from subprocess import Popen
from time       import time

import mon

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'

#
# configs and reports
#

class Stats(object):
	__start: float
	__end:   float

	def __init__(s):
		s.__start = time()

	def end(s):
		s.__end = time()

	def took(s) -> float:
		return s.__end - s.__start

def _print(*args):
	print(*args)

def _config(sts):
	cluster = mon.cluster()
	_print('multigraph mnppl')
	_print(f"graph_title {cluster} mnppl")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category munin')
	_print('graph_vlabel seconds')
	_print('graph_printf %3.3lf')
	_print('graph_scale yes')
	color = -1
	for pl in sts.keys():
		color = mon.color(color)
		fn = mon.cleanfn(pl)
		_print('%s.label' % fn, pl)
		_print('%s.colour COLOUR%d' % (fn, color))
		_print('%s.draw AREA' % fn)
		_print('%s.min 0' % fn)
		_print('%s.warning 270' % fn)
		_print('%s.critical 290' % fn)

def _report(sts):
	_print('multigraph mnppl')
	# FIXME: loop sts keys
	for pl in sts.keys():
		fn = mon.cleanfn(pl)
		_print('%s.value' % fn, sts[pl].took())

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
		sys.stdout.write('\n')
		sys.stdout.flush()

def _run(bindir: str, action: str, self_report: bool = False) -> int:
	sts: dict[str, Stats] = {}
	pwait: dict[str, Popen] = {}
	for pl in _listPlugins(bindir):
		if self_report:
			sts[pl] = Stats()
		cmd = [Path(bindir, pl).as_posix()]
		if action == 'config':
			cmd.append(action)
		pwait[pl] = _newProc(cmd)
	rc = 0
	for pl, proc in pwait.items():
		st = proc.wait()
		if st != 0:
			rc = st
		_pprint(proc)
		if self_report:
			sts[pl].end()
	if self_report:
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
	flags.add_argument('-R', '--no-report', action = 'store_true', default = False,
		help = 'no self report')
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
		self_report = not args.no_report
		return _run(args.bindir, action, self_report = self_report)
	return rc

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
