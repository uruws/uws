# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import wapp

#-------------------------------------------------------------------------------
# config

cmdpath:   Path = Path('/usr/bin/ab')
user_agent: str = '-HUser-Agent:uwsab'

#-------------------------------------------------------------------------------
# command

class Command(object):
	cmdargs:      list[str]
	requests:     int = 1
	concurrency:  int = 1
	timelimit:    int = 0
	timeout:      int = 7
	postfile:     str = ''
	content_type: str = ''
	_id:          str = ''

	def __init__(c, *args):
		c.cmdargs = [str(a) for a in args]

	def __str__(c) -> str:
		args = c.args()
		args.remove(user_agent)
		if c._id != '':
			return '%s: %s' % (c._id, ' '.join(args))
		return '%s' % ' '.join(args)

	def id(c) -> str:
		return c._id

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
		a.append(user_agent)
		a.extend([str(a) for a in list(c.cmdargs)])
		return a

	def run(c) -> wapp.NQJob:
		q = wapp.NQ('run')
		q.cleanup = False
		return q.run(c.args())

def command_parse(_id: str, args: str) -> Command:
	c = Command()
	c._id = _id.strip()
	add = False
	for a in args.split(' '):
		a = a.strip()
		if a == str(cmdpath):
			add = True
			continue
		if a.startswith('-H'):
			continue
		if a.startswith('-n'):
			c.requests = int(a[2:])
			continue
		if a.startswith('-c'):
			c.concurrency = int(a[2:])
			continue
		if a.startswith('-t'):
			c.timelimit = int(a[2:])
			continue
		if a.startswith('-s'):
			c.timeout = int(a[2:])
			continue
		if a.startswith('-p'):
			c.postfile = str(a[2:])
			continue
		if a.startswith('-T'):
			c.content_type = str(a[2:])
			continue
		if add:
			c.cmdargs.append(a)
	return c

class CommandForm(Command):

	def items(f):
		return dict(
			requests    = str(f.requests),
			concurrency = str(f.concurrency),
			timelimit   = str(f.timelimit),
			timeout     = str(f.timeout),
		).items()

	def parse(f, req) -> Command:
		url = 'https://%s' % req.get('abench_url', 'NO_URL')
		cmd = Command(url)
		cmd.requests    = int(req.get('abench_requests',    f.requests))
		cmd.concurrency = int(req.get('abench_concurrency', f.concurrency))
		cmd.timelimit   = int(req.get('abench_timelimit',   f.timelimit))
		cmd.timeout     = int(req.get('abench_timeout',     f.timeout))
		return cmd
