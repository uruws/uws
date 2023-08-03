# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

from pathlib import Path

import wapp

#-------------------------------------------------------------------------------
# config

cmdpath: str = '/opt/uws/ab/abrun.py'

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
	_parsed:     bool = False
	_command:     str = ''
	_start_time:  str = ''
	_end_time:    str = ''
	_took:      float = 0.0
	_failed:      int = 0
	_rps:       float = 0.0
	_tpr:       float = 0.0

	def __init__(c, *args):
		c.cmdargs = [str(a) for a in args]

	def __str__(c) -> str:
		args = c.args()
		if c._id != '':
			return '%s: %s' % (c._id, ' '.join(args))
		return '%s' % ' '.join(args)

	def id(c) -> str:
		return c._id

	def args(c) -> list[str]:
		a = [cmdpath.strip()]
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
		a.extend([str(a) for a in list(c.cmdargs)])
		return a

	def _nq(c) -> wapp.NQ:
		return wapp.NQ('run')

	def run(c) -> wapp.NQJob:
		q = c._nq()
		q.cleanup = False
		return q.run(c.args())

	def _parse_int(c, line) -> int:
		i = line.split(':')
		n = i[1].strip().split()[0].strip()
		return int(n)

	def _parse_float(c, line) -> float:
		i = line.split(':')
		n = i[1].strip().split()[0].strip()
		return float(n)

	def _parse(c):
		if c._parsed:
			return
		c.concurrency = 0
		c.requests    = 0
		q = c._nq()
		for line in q.read(c._id).splitlines():
			line = line.strip()
			if line.startswith('exec '):
				c._command = str(line)
			elif line.startswith('Start: '):
				c._start_time = str(line[7:])
			elif line.startswith('End: '):
				c._end_time = str(line[5:])
			elif line.startswith('Concurrency Level:'):
				c.concurrency = c._parse_int(line)
			elif line.startswith('Complete requests:'):
				c.requests = c._parse_int(line)
			elif line.startswith('Time taken for tests:'):
				c._took = c._parse_float(line)
			elif line.startswith('Failed requests:'):
				c._failed = c._parse_int(line)
			elif line.startswith('Requests per second:'):
				c._rps = c._parse_float(line)
			elif line.startswith('Time per request:'):
				c._tpr = c._parse_float(line)
		c._parsed = True

	def command(c) -> str:
		c._parse()
		return c._command

	def start_time(c) -> str:
		c._parse()
		return c._start_time

	def end_time(c) -> str:
		c._parse()
		return c._end_time

	def took(c) -> float:
		c._parse()
		return c._took

	def failed(c) -> int:
		c._parse()
		return c._failed

	def rps(c) -> float:
		"""Request per second."""
		c._parse()
		return c._rps

	def tpr(c) -> float:
		"""Time per request."""
		c._parse()
		return c._tpr

def command_parse(_id: str, args: str) -> Command:
	c = Command()
	c._id = _id.strip()
	add = False
	for a in args.split(' '):
		a = a.strip()
		if a == cmdpath:
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
