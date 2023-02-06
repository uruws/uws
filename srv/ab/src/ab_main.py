# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
from   bottle import response
from   bottle import template

import ab
import ab_conf

app = bottle.Bottle()

#
# views
#

@app.get('/healthz')
def healthz():
	response.content_type = 'text/plain'
	cmd = ab.Command('--help')
	rc = ab.run(cmd)
	if rc != 22:
		return 'error: %d' % rc
	return 'ok'

@app.get('/')
def home():
	return template('home.html')

#
# main
#

def wsgi_application():
	return app

def main():
	app.run(
		host     = '0.0.0.0',
		port     = ab.webapp_port,
		reloader = ab.debug,
		debug    = ab.debug,
	)

if __name__ == '__main__': # pragma: no cover
	main()
