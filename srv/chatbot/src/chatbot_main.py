# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import os

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
	if os.getenv('UWS_WEBAPP_DEBUG', 'off') == 'on':
		logging.basicConfig(level = logging.DEBUG)
	logging.debug('slack connect')
	chatbot_slack.connect()
	chatbot_slack.msg('connected')

def getapp():
	start()
	return bottle.app

def main():
	start()
	logging.debug('started')
	listen_port = int(os.getenv('UWS_WEBAPP_PORT', '2741'))
	logging.debug('bottle run')
	bottle.run(host = '0.0.0.0', port = listen_port, reloader = True, debug = True)

if __name__ == '__main__': # pragma: no cover
	main()
