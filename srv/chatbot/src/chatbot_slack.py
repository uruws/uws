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

@app.event("app_mention")
def event_app_mention(event, say):
	user_id = event['user']
	say(f"Hello <@{user_id}>!!")

@app.event("app_home_opened")
def event_app_home_opened(body, logger):
	logger.debug(body)

if __name__ == '__main__':
	logging.basicConfig(level = logging.DEBUG)
	logging.debug('start')
	SocketModeHandler(app, os.getenv('SLACK_APP_TOKEN')).start()
