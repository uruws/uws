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
from subprocess import TimeoutExpired
from time       import time

import mon

plugins_bindir = '/usr/local/bin'
plugins_suffix = '.mnppl'
time_warning   = 270
time_critical  = 290
plwait_timeout = 240

#
# configs and reports
#

def _print(*args):
	print(*args)

def _config():
	cluster = mon.cluster()
	_print('multigraph mnppl')
	_print(f"graph_title {cluster} mnppl")
	_print('graph_args --base 1000 -l 0')
	_print('graph_category munin')
	_print('graph_vlabel seconds')
	_print('graph_printf %3.3lf')
	_print('graph_scale yes')
	_print('mnppl.label total')
	_print('mnppl.colour COLOUR0')
	_print('mnppl.draw AREA')
	_print('mnppl.min 0')
	_print('mnppl.warning', time_warning)
	_print('mnppl.critical', time_critical)

def _report(elapsed_time: float):
	_print('multigraph mnppl')
	_print('mnppl.value', elapsed_time)

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
	# ~ return Popen(cmd, text = True, stdout = PIPE, stderr = PIPE)
	return Popen(cmd, text = True)

def _pprint(p: Popen) -> bool:
	_done = False
	pl = Path(str(p.args[0])).name
	name = Path(pl).stem
	if p.returncode != 0:
		print('[ERROR]', pl, 'failed:', p.returncode, file = sys.stderr)
		sys.stderr.flush()
		_done = True
	# ~ if p.stderr is not None:
		# ~ for line in p.stderr.readlines():
			# ~ sys.stderr.write('[E] %s: ' % name)
			# ~ sys.stderr.write(line)
		# ~ p.stderr.close()
		# ~ sys.stderr.flush()
		# ~ _done = True
	# ~ if p.stdout is not None:
		# ~ sys.stdout.write(p.stdout.read())
		# ~ p.stdout.close()
		# ~ sys.stdout.flush()
		# ~ _done = True
	return _done

def _run(bindir: str, action: str) -> int:
	run_start: float = time()
	pwait: dict[str, Popen] = {}
	for pl in _listPlugins(bindir):
		mon.dbg('pl:', pl)
		cmd = [Path(bindir, pl).as_posix()]
		if action == 'config':
			cmd.append(action)
		pwait[pl] = _newProc(cmd)
	rc = 0
	for pl, proc in pwait.items():
		mon.dbg('pwait:', pl)
		try:
			st = proc.wait(timeout = plwait_timeout)
			if st != 0:
				rc = st
			_pprint(proc)
		except TimeoutExpired as err:
			mon.log('[ERROR]', err)
			proc.kill()
	if action == 'config':
		_config()
	else:
		_report(time() - run_start)
	return rc

#
# main
#

__doc__ = 'munin-node parallel plugins runner'

def main(argv: list[str]) -> int:
	flags = ArgumentParser(description = __doc__)

	flags.add_argument('-b', '--bindir', default = plugins_bindir,
		help = 'plugins bindir')
	flags.add_argument('action', default = 'report', nargs = '*',
		choices = ['config', 'report'],
		help = 'plugin action')

	args = flags.parse_args(argv)

	action = 'report'
	if isinstance(args.action, list):
		action = args.action[0].strip()

	return _run(args.bindir, action)

if __name__ == '__main__': # pragma no cover
	sys.exit(main(sys.argv[1:]))
