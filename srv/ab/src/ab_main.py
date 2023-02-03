# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore

import ab_conf
import ab

app = bottle.Bottle()

#
# views
#

@app.post('/healthz')
def healthz():
	return 'OK'

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
