# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle
import logging
import os

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
	try:
		# FIXME: validate Slack request
		d = dict(bottle.request.json)
		c = d.get('challenge', '')
		return c.strip()
	except Exception as err:
		logging.error(err)
	return handler.handle(bottle.request, bottle.response)

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG)
	listen_port = int(os.getenv('UWS_WEBAPP_PORT', '2741'))
	bottle.run(host = '0.0.0.0', port = listen_port, reloader = True)
