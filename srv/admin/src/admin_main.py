# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import wapp

import admin_conf # just load it

import admin
import admin_views

import admintpl # just load it

app = wapp.Bottle()
log = wapp.getLogger(__name__)

def start():
	wapp.start(app)
	log.debug('start')
	admin_views.start(app)

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
