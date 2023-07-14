# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import subprocess
import sys

from os      import getenv
from pathlib import Path

#
# config
#

cmdpath: Path = Path('/usr/bin/ab')

#
# command
#

class Command(object):
	cmdargs:      list[str]
	requests:     int       = 0
	concurrency:  int       = 0
	timelimit:    int       = 0
	timeout:      int       = 0
	postfile:     str       = ''
	content_type: str       = ''

	def __init__(c, *args):
		c.cmdargs = args

	def args(c) -> list[str]:
		a = [cmdpath.as_posix()]
		a.extend([str(a) for a in list(c.cmdargs)])
		if c.requests != 0:
			a.append('-n%d' % c.requests)
		if c.concurrency != 0:
			a.append('-c%d' % c.concurrency)
		if c.timelimit != 0:
			a.append('-t%d' % c.timelimit)
		if c.timeout != 0:
			a.append('-s%d' % c.timeout)
		if c.postfile != '':
			a.append('-p%s' % c.postfile)
		if c.content_type != '':
			a.append('-T%s' % c.content_type)
		a.append('-HUser-Agent: uwsab')
		return a

#
# api
#

def run(cmd: Command, timeout: int = 15) -> int:
	if cmd.timelimit > 0:
		timeout = cmd.timelimit + timeout
	try:
		proc = subprocess.run(cmd.args(), check = True, timeout = timeout,
			capture_output = True)
	except subprocess.CalledProcessError as err:
		return err.returncode
	except subprocess.TimeoutExpired:
		print('[ERROR] subprocess timeout:', cmd.args(), file = sys.stderr)
		return 9
	return 0
