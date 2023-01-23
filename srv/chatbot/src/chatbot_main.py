# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import sys

from pathlib import Path

import chatbot_conf

import chatbot
import chatbot_slack

#
# views
#

@bottle.post('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return 'OK'
	raise RuntimeError('slack chatbot not healthy')

#
# main
#

def start():
	if chatbot.debug:
		logging.basicConfig(level = logging.DEBUG)
	logging.debug('start')
	chatbot_slack.connect()
	logging.debug('slack connected')
	chatbot_slack.msg('connected')

def getapp():
	start()
	logging.debug('getapp')
	return bottle.app[0]

def main():
	start()
	logging.debug('bottle run')
	bottle.run(
		host     = '0.0.0.0',
		port     = chatbot.webapp_port,
		reloader = True,
		debug    = True,
	)

if __name__ == '__main__': # pragma: no cover
	main()
