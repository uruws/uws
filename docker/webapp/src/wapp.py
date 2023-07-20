# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import os

from bottle import Bottle
from bottle import request
from bottle import response
from bottle import template

from logging import Logger

__all__ = [
	'Bottle',
	'Logger',
	'request',
	'response',
	'template',
]

from pathlib import Path
from shutil  import rmtree

log: Logger = logging.getLogger(__name__)

#
# globals
#

name:   str =     os.getenv('UWS_WEBAPP',       'default')
debug: bool =     os.getenv('UWS_WEBAPP_DEBUG', 'off') == 'on'
port:   int = int(os.getenv('UWS_WEBAPP_PORT',  '2741'))
nqdir:  str =     os.getenv('UWS_WEBAPP_NQDIR', '/tmp/wappnq')

#
# logging
#

# https://docs.python.org/3.9/library/logging.html#logrecord-attributes
logfmt_debug = '%(pathname)s:%(lineno)d %(message)s'

def getLogger(name: str) -> logging.Logger:
	return logging.getLogger(name)

#
# bottle
#

def bottle_start(app: str):
	log.debug('bottle_start: %s', app)
	bottle.TEMPLATE_PATH = [
		Path('/opt/uws/lib/views'),
		Path('/opt/uws', app, 'views'),
	]

def static_files_handler(app: Bottle, name: str):
	log.debug('static files handler: %s', name)

	@app.get('/static/%s/<filename:path>' % name)
	def app_static(filename): # pragma: no cover
		return bottle.static_file(filename, root = Path('/opt/uws', name, 'static', name))

	@app.get('/static/<filename:path>')
	def lib_static(filename): # pragma: no cover
		return bottle.static_file(filename, root = Path('/opt/uws/lib/static'))

#
# main
#

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

#
# nq
#

class NQ(object):
	name:         str
	app:          str = ''
	dir:  Path | None = None

	def __init__(q, qname: str, app: str = name):
		q.name = qname
		q.app = app
		q.dir = Path(nqdir, q.app, q.name)
		q._setup()

	def _setup(q):
		q.dir.mkdir(mode = 0o0750, parents = True, exist_ok = True)
		q.dir.chmod(0o0750) # in case it already exists

	def delete(q):
		rmtree(q.dir)
