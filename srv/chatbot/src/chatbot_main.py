# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle
import logging

from slack_bolt                import App
from slack_bolt.adapter.bottle import SlackRequestHandler

bot = App()

@bot.middleware
def log_request(logger, body, next):
	logger.debug(body)
	return next()

@bot.event('app_mention')
def event_app_mention(ack, body, say, logger):
	logger.info(body)
	say("What's up?")

handler = SlackRequestHandler(bot)

@bottle.post('/slack/events')
def slack_events():
	return handler.handle(bottle.request, bottle.response)

def _setLogLevel():
	logging.basicConfig(level = logging.DEBUG)

def _listenPort():
	return int(os.getenv('UWS_WEBAPP_PORT', '2741'))

if __name__ == '__main__':
	_setLogLevel()
	bottle.run(host = '0.0.0.0', port = _listenPort(), reloader = True)
