# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# https://github.com/slackapi/bolt-python/blob/main/examples/socket_mode.py

import os

from slack_bolt                     import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import wapp

import chatbot
import chatbot_msg

log = wapp.getLogger(__name__)

app = App(
	token = os.getenv('SLACK_BOT_TOKEN'),
)

#-------------------------------------------------------------------------------
# utils
# /opt/uws/venv/bin/python3 -m pydoc slack_sdk.WebClient

channel_id: str = os.getenv('UWS_SLACK_CHANNEL_ID', '')

def msg(text: str):
	log.debug('%s: send message', channel_id)
	res = app.client.chat_postMessage(channel = channel_id, text = text)
	if not res.get('ok', False):
		log.error('%s: send message failed: %s', channel_id, res)

def attach(ts: str, text: str, content: str):
	log.debug('%s: %s attach', channel_id, ts)
	res = app.client.files_upload(channels = channel_id, thread_ts = ts,
		content = content, initial_comment = text, filetype = 'text/plain',
		title = 'output.txt', filename = 'output.txt')
	if not res.get('ok', False):
		log.error('%s: %s attach failed: %s', channel_id, ts, res)

#-------------------------------------------------------------------------------
# events

# https://api.slack.com/messaging/sending
# https://api.slack.com/events/message
# https://api.slack.com/messaging/composing
# https://github.com/slackapi/bolt-python/blob/main/examples/message_events.py

def _message(event, say, mention = False) -> str:
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
			proc = chatbot.uwscli(user_id, text)
		except chatbot.UwscliCmdError as err:
			log.debug('UwscliCmdError%s', err)
			if mention:
				say(f"{user_mention}invalid command: {text}", thread_ts = thread_ts)
			return 'error'
		if proc.status != 0:
			st = '[ERROR] '
			log.error('uwscli command failed (%d): %s', proc.status, text)
			log.debug('%s[%d]: %s', proc.command, proc.status, proc.output)
		# parse response message content
		msgid = 0
		msgt, output = chatbot_msg.check(proc.output)
		if msgt == 'attach':
			attach(thread_ts, text, output)
		else:
			# msgt == 'message'
			for msg in chatbot_msg.parse(text, output):
				if msgid == 0:
					say(f"{user_mention}{st}{msg}", thread_ts = thread_ts)
				else:
					say(f"{st}{msg}", thread_ts = thread_ts)
				msgid += 1
		return msgt
	return ''

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

@app.event('app_mention')
def event_app_mention(event, say):
	log.debug('event_app_mention')
	_message(event, say, mention = True)

@app.event('app_home_opened')
def event_app_home_opened(body):
	log.debug('app_home_opened: %s', body)

#-------------------------------------------------------------------------------
# socket mode handler

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
