# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# https://github.com/slackapi/bolt-python/blob/main/examples/

import logging
import os

from slack_bolt import App

log = logging.getLogger(__name__)

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
