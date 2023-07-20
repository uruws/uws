# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

import ab
import ab_conf

import ab_views

app = wapp.Bottle()
log = wapp.getLogger(__name__)

def start():
	wapp.start(app)
	log.debug('start')
	ab_views.start(app)

def wsgi_application():
	start()
	log.debug('wsgi app')
	return app

def main():
	start()
	log.debug('bottle run')
	wapp.run(app)

if __name__ == '__main__': # pragma: no cover
	main()
