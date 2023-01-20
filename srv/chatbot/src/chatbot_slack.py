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

#
# events
#

@app.event('app_mention')
def event_app_mention(event, say):
	logging.debug('app_mention: %s', event)
	user_id = event['user']
	text = ' '.join(event.get('text', '').split(' ')[1:])
	thread_ts = event.get('thread_ts', None) or event['ts']
	logging.debug('app_mention reply: %s', thread_ts)
	say(f"<@{user_id}>: {text}", thread_ts = thread_ts)

@app.event('app_home_opened')
def event_app_home_opened(body):
	logging.debug('app_home_opened: %s', body)

# https://api.slack.com/events/message
# https://github.com/slackapi/bolt-python/blob/main/examples/message_events.py

@app.event('message')
def event_message(body, say):
	logging.debug('message: %s', body)
	event = body['event']
	thread_ts = event.get('thread_ts', None)
	if thread_ts is not None:
		logging.debug('message reply: %s', thread_ts)
		say(text = "Sorry, I'am not that clever.", thread_ts = thread_ts)
	else:
		logging.info('message ignored')

#
# socket mode handler
#

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

#
# utils
#

channel_id: str = os.getenv('UWS_CHATBOT_CHANNEL_ID', '')

def msg(text: str):
	logging.debug('send message: %s', channel_id)
	res = app.client.chat_postMessage(channel = channel_id, text = text)
	if not res.get('ok', False):
		logging.error('send message failed: %s', res)
