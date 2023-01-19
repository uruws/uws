# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle
import logging
import os

import chatbot_slack

@bottle.post('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return 'OK'
	raise RuntimeError('slack chatbot not healthy')

def getapp():
	return bottle.app

if __name__ == '__main__':
	if os.getenv('UWS_WEBAPP_DEBUG', 'off') == 'on':
		logging.basicConfig(level = logging.DEBUG)
	listen_port = int(os.getenv('UWS_WEBAPP_PORT', '2741'))
	chatbot_slack.connect()
	bottle.run(host = '0.0.0.0', port = listen_port, reloader = True)
