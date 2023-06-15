# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import sys

from pathlib import Path

import chatbot_conf

import chatbot
import chatbot_slack

app = bottle.Bottle()
log = logging.getLogger(__name__)

# https://docs.python.org/3.9/library/logging.html#logrecord-attributes
logfmt       = '%(message)s'
logfmt_debug = '%(pathname)s:%(lineno)d %(message)s'

#
# views
#

@app.get('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return 'ok'
	raise RuntimeError('slack chatbot not healthy')

#
# main
#

def start():
	logging.basicConfig(format = logfmt)
	if chatbot.debug:
		logging.basicConfig(format = logfmt_debug, level = logging.DEBUG)
	log.debug('start')
	chatbot_slack.connect()
	log.debug('slack connected')
	chatbot_slack.msg('connected')

def wsgi_application():
	start()
	log.debug('wsgi application: %s', type(app))
	return app

def main():
	start()
	log.debug('bottle run')
	app.run(
		host     = '0.0.0.0',
		port     = chatbot.webapp_port,
		reloader = chatbot.debug,
		debug    = chatbot.debug,
	)

if __name__ == '__main__': # pragma: no cover
	main()
