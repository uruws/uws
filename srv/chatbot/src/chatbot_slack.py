# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# https://github.com/slackapi/bolt-python/blob/main/examples/socket_mode.py

import logging
import os

from slack_bolt                     import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(
	token = os.getenv('SLACK_BOT_TOKEN'),
)

@app.event('app_mention')
def event_app_mention(event, say):
	logging.debug('app_mention: %s', event)
	user_id = event['user']
	say(f"Hello <@{user_id}>!!")

@app.event('app_home_opened')
def event_app_home_opened(body):
	logging.debug('app_home_opened: %s', body)

@app.event('message')
def event_message(body):
	logging.debug('message: %s', body)

smh = SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN'))

def connect():
	smh.connect()

def is_healthy() -> bool:
	if smh.client is None:
		logging.error('no socket mode handler client')
		return False
	if not smh.client.is_connected():
		logging.error('socket mode handler client not connected')
		return False
	return True
