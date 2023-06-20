# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# https://github.com/slackapi/bolt-python/blob/main/examples/socket_mode.py

import logging
import os

from slack_bolt                     import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import chatbot

log = logging.getLogger(__name__)

app = App(
	token = os.getenv('SLACK_BOT_TOKEN'),
)

#
# events
#

@app.event('app_home_opened')
def event_app_home_opened(body):
	log.debug('app_home_opened: %s', body)

# https://api.slack.com/events/message
# https://github.com/slackapi/bolt-python/blob/main/examples/message_events.py

def _message(event, say, mention = False):
	log.debug('message: %s', event)
	user_id = event['user']
	if mention:
		text = ' '.join(event.get('text', '').split(' ')[1:]).strip()
		user_mention = f"<@{user_id}>: "
	else:
		text = event.get('text', '').strip()
		user_mention = ''
	thread_ts = event.get('thread_ts', None) or event['ts']
	log.debug('message reply: %s', thread_ts)
	if text == '':
		say(f"<@{user_id}>: what do you mean?", thread_ts = thread_ts)
	else:
		st = ''
		try:
			rc, out = chatbot.uwscli(user_id, text)
		except chatbot.UwscliCmdError:
			log.debug('uwscli ignore: %s', text)
			say(f"{user_mention}invalid command", thread_ts = thread_ts)
			return
		if rc != 0:
			st = '[ERROR] '
			log.error('uwscli command failed (%d): %s', rc, text)
			log.debug('%s', out)
		say(f"{user_mention}{st}{text}\n```\n{out}\n```", thread_ts = thread_ts)

@app.event('app_mention')
def event_app_mention(event, say):
	log.debug('event_app_mention')
	_message(event, say, mention = True)

@app.event('message')
def event_message(body, say):
	log.debug('event_message')
	event = body['event']
	thread_ts = event.get('thread_ts', None)
	if thread_ts is not None:
		log.debug('message reply: %s', thread_ts)
		_message(event, say)
	else:
		log.info('message ignored')

#
# socket mode handler
#

smh = SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN'))

def connect():
	smh.connect()

def is_healthy() -> bool:
	if smh.client is None:
		log.error('no socket mode handler client')
		return False
	if not smh.client.is_connected():
		log.error('socket mode handler client not connected')
		return False
	return True

#
# utils
#

channel_id: str = os.getenv('UWS_SLACK_CHANNEL_ID', '')

def msg(text: str):
	log.debug('send message: %s', channel_id)
	res = app.client.chat_postMessage(channel = channel_id, text = text)
	if not res.get('ok', False):
		log.error('send message failed: %s', res)
