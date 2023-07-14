# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
from   bottle import response
from   bottle import template

import wapp

import ab
import ab_conf

app = wapp.Bottle()
log = wapp.getLogger(__name__)

#
# views
#

@app.get('/healthz')
def healthz():
	response.content_type = 'text/plain'
	cmd = ab.Command('--help')
	rc = ab.run(cmd)
	if rc != 22:
		raise RuntimeError('ab exit status: %d' % rc)
	return 'ok'

@app.get('/')
def home():
	return template('home.html')

#
# main
#

def start():
	wapp.start('ab', debug = ab.debug)
	log.debug('start')

def wsgi_application():
	start()
	log.debug('wsgi app')
	return app

def main():
	start()
	log.debug('bottle run')
	app.run(
		host     = '0.0.0.0',
		port     = ab.webapp_port,
		reloader = ab.debug,
		debug    = ab.debug,
	)

if __name__ == '__main__': # pragma: no cover
	main()
