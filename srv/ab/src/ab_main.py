# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
from bottle import response

import ab_conf
import ab

app = bottle.Bottle()

#
# views
#

@app.get('/healthz')
def healthz():
	response.content_type = 'text/plain'
	return u'ok'

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
