# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import os
import subprocess

from bottle import Bottle
from bottle import redirect
from bottle import request
from bottle import response
from bottle import template

from logging import Logger

__all__ = [
	'Bottle',
	'Logger',
	'redirect',
	'request',
	'response',
	'template',
]

from pathlib import Path
from shutil  import rmtree

log: Logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# globals

name:     str =     os.getenv('UWS_WEBAPP',       'default').strip()
debug:   bool =     os.getenv('UWS_WEBAPP_DEBUG', 'off').strip() == 'on'
port:     int = int(os.getenv('UWS_WEBAPP_PORT',  '2741').strip())
base_url: str =     os.getenv('UWS_WEBAPP_URL',   '/').strip()

#-------------------------------------------------------------------------------
# logging
# https://docs.python.org/3.9/library/logging.html#logrecord-attributes

logfmt_debug = '%(pathname)s:%(lineno)d %(message)s'

def getLogger(name: str) -> logging.Logger:
	return logging.getLogger(name)

#-------------------------------------------------------------------------------
# utils

def url(path: str) -> str:
	"""generate URLs"""
	if base_url == '/':
		return path.strip()
	return '%s%s' % (base_url, path.strip())

def error(status: int, tpl: str, **kwargs):
	"""return templated error status page"""
	response.status = status
	return template(tpl, **kwargs)

#-------------------------------------------------------------------------------
# bottle

def bottle_start(app: str):
	if debug:
		bottle.DEBUG = True
	log.debug('bottle_start: %s', app)
	bottle.TEMPLATE_PATH = [
		Path('/opt/uws/lib/views'),
		Path('/opt/uws', app, 'views'),
	]

def static_files_handler(app: Bottle, name: str):
	log.debug('static files handler: %s', name)

	@app.get(url('/static/%s/<filename:path>' % name))
	def app_static(filename): # pragma: no cover
		return bottle.static_file(filename, root = Path('/opt/uws', name, 'static', name))

	@app.get(url('/static/<filename:path>'))
	def lib_static(filename): # pragma: no cover
		return bottle.static_file(filename, root = Path('/opt/uws/lib/static'))

#-------------------------------------------------------------------------------
# main

def start(app: Bottle):
	if debug:
		logging.basicConfig(format = logfmt_debug, level = logging.DEBUG)
	log.debug('start: %s', name)
	bottle_start(name)
	static_files_handler(app, name)

def run(app: Bottle):
	app.run(
		host     = '0.0.0.0',
		port     = port,
		reloader = debug,
		debug    = debug,
	)

#-------------------------------------------------------------------------------
# nq

fqcmd: str = os.getenv('UWS_WEBAPP_FQCMD', '/usr/bin/fq')
nqcmd: str = os.getenv('UWS_WEBAPP_NQCMD', '/usr/bin/nq')
nqdir: str = os.getenv('UWS_WEBAPP_NQDIR', '/tmp/wappnq')

class NQJobInfo(object):
	_line:  str
	_nqdir: str = ''
	_id:    str = ''

	def __init__(j, fqline: str, qdir: str = nqdir):
		j._line  = fqline.strip()
		j._nqdir = nqdir.strip()
		if j._line.startswith('==> ,'):
			j._id = fqline.split(' ')[1].strip()[1:]

	def __str__(j) -> str:
		return j._line

	def id(j):
		return j._id

class NQJob(object):
	proc: subprocess.CompletedProcess
	_id:  str = ''

	def __init__(j, proc: subprocess.CompletedProcess):
		j.proc = proc

	def rc(j) -> int:
		return j.proc.returncode

	def id(j) -> str:
		if j._id == '':
			return j.proc.stdout.strip()
		return j._id

	def error(j) -> str:
		return j.proc.stderr.strip()

def _fqrun(env: dict[str, str]) -> list[str]:
	cmd = '%s -qan' % fqcmd
	proc = subprocess.run(cmd, shell = True, env = env,
		encoding = 'utf-8', text = True, capture_output = True)
	return [l.strip() for l in proc.stdout.splitlines()]

def _nqrun(cmd: str, env: dict[str, str] | None = None) -> NQJob:
	return NQJob(subprocess.run(cmd, shell = True, env = env,
		encoding = 'utf-8', text = True, capture_output = True))

def _nqsetup(qdir: str):
	dh = Path(qdir)
	dh.mkdir(mode = 0o0750, parents = True, exist_ok = True)
	dh.chmod(0o0750) # in case it already existed

class NQ(object):
	name:    str
	app:     str = ''
	dir:     str = ''
	cleanup: bool = True
	quiet:   bool = True

	def __init__(q, qname: str, app: str = name):
		q.name = qname
		q.app = app
		q.dir = str(Path(nqdir, q.app, q.name))
		_nqsetup(q.dir)

	def delete(q):
		rmtree(q.dir)

	def env(q) -> dict[str, str]:
		return {
			'USER':  os.environ.get('USER', 'uws'),
			'HOME':  os.environ.get('HOME', '/home/uws'),
			'PATH':  '/usr/bin',
			'NQDIR': q.dir,
		}

	def args(q) -> str:
		a = ' '
		if q.cleanup:
			a += '-c '
		if q.quiet:
			a += '-q '
		return a

	def run(q, args: list[str]) -> NQJob:
		cmd = '%s%s%s' % (nqcmd, q.args(), ' '.join(args))
		return _nqrun(cmd, env = q.env())

	def list(q) -> list[NQJobInfo]:
		l: list[NQJobInfo] = []
		for s in _fqrun(q.env()):
			l.append(NQJobInfo(s, q.dir))
		return l

	def read(q, jobid: str) -> str:
		fh = Path(q.dir, ',%s' % jobid)
		return fh.read_text()
