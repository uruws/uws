# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

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
	requests:     int       = 1
	concurrency:  int       = 1
	timelimit:    int       = 0
	timeout:      int       = 7
	postfile:     str       = ''
	content_type: str       = ''

	def __init__(c, *args):
		c.cmdargs = args

	def args(c) -> list[str]:
		a = [cmdpath.as_posix()]
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
		a.append('-HUser-Agent:uwsab')
		a.extend([str(a) for a in list(c.cmdargs)])
		return a
