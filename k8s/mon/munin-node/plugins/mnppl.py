#!/usr/bin/env python3

# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import os
import sys

MONLIB = os.getenv('MONLIB', '/srv/munin/plugins')
sys.path.insert(0, MONLIB)

from argparse   import ArgumentParser
from pathlib    import Path
from subprocess import PIPE
from subprocess import Popen
from time       import time

from multiprocessing.pool import Pool

import mon

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'
pool_wait      = 300
time_warning   = 270
time_critical  = 290

#
# configs and reports
#

def _print(*args):
	print(*args)

def _config(sts: dict[str, float]):
	cluster = mon.cluster()
	_print('multigraph mnppl')
	_print(f"graph_title {cluster} mnppl")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category munin')
	_print('graph_vlabel seconds')
	_print('graph_printf %3.3lf')
	_print('graph_scale yes')
	# total
	fn = mon.cleanfn('total.mnppl')
	_print('%s.label total' % fn)
	_print('%s.colour COLOUR0' % fn)
	_print('%s.draw LINE' % fn)
	_print('%s.min 0' % fn)
	_print('%s.max 400' % fn)
	_print('%s.warning' % fn, time_warning)
	_print('%s.critical' % fn, time_critical)
	# plugins
	color = 0
	for pl in sorted(sts.keys()):
		color = mon.color(color)
		fn = mon.cleanfn(pl)
		_print('%s.label' % fn, Path(pl).stem)
		_print('%s.colour COLOUR%d' % (fn, color))
		_print('%s.draw AREA' % fn)
		_print('%s.min 0' % fn)
		_print('%s.max 400' % fn)

def _report(sts: dict[str, float]):
	_print('multigraph mnppl')
	for pl in sorted(sts.keys()):
		fn = mon.cleanfn(pl)
		_print('%s.value' % fn, sts.get(pl, 'U'))

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

class Proc(object):
	cmd:   list[str]
	err:   str
	out:   str
	name:  str
	start: float
	end:   float
	rc:    int

	def __init__(p, cmd: list[str]):
		p.cmd  = cmd.copy()
		p.pl   = Path(p.cmd[0]).name
		p.name = Path(p.pl).stem
		p.err  = ''
		p.out  = ''
		p.rc   = -128

	def print(p):
		if p.rc != 0:
			print('[ERROR]', p.pl, 'failed:', p.rc, file = sys.stderr)
			sys.stderr.flush()
		if p.err != '':
			for line in p.err.splitlines(keepends = True):
				sys.stderr.write('[E] %s: ' % p.pl)
				sys.stderr.write(line)
			sys.stderr.flush()
		if p.out != '':
			sys.stdout.write(p.out)
			sys.stdout.flush()

	def took(p) -> float:
		return p.end - p.start

def _start(cmd: list[str]) -> Proc:
	p = Proc(cmd)
	p.start = time()
	x = _newProc(p.cmd)
	p.rc = x.wait()
	if x.stderr is not None:
		p.err = x.stderr.read()
		x.stderr.close()
	if x.stdout is not None:
		p.out = x.stdout.read()
		x.stdout.close()
	p.end = time()
	return p

def _run(bindir: str, action: str, self_report: bool = True) -> int:
	run_start: float = time()
	x: list[list[str]] = []
	for pl in _listPlugins(bindir):
		cmd = [Path(bindir, pl).as_posix()]
		if action == 'config':
			cmd.append(action)
		x.append(cmd)
	xlen = len(x)
	if xlen < 1:
		print('[ERROR] mnppl: no plugins to run', file = sys.stderr)
		return 1
	sts: dict[str, float] = {}
	with Pool(processes = xlen) as pool:
		rwait = []
		for i in range(xlen):
			r = pool.apply_async(_start, (x[i],))
			rwait.append(r)
		for i in range(xlen):
			r = rwait[i]
			r.wait(pool_wait)
			p = r.get()
			p.print()
			if self_report:
				sts[p.pl] = p.took()
	if self_report:
		if action == 'config':
			_config(sts)
		else:
			sts['total.mnppl'] = time() - run_start
			_report(sts)
	return 0

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
			st = mon.system(Path(args.bindir, pl))
			if st != 0:
				rc = st
	else:
		self_report = not args.no_report
		return _run(args.bindir, action, self_report = self_report)
	return rc

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
