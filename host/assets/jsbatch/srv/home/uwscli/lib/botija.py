# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

# /opt/uws/venv/bin/python3 -m pydoc slack_sdk.WebClient

import logging
import os
import sys

from slack_bolt import App # type: ignore

log = logging.getLogger(__name__)

app = App(
	token = os.getenv('SLACK_BOT_TOKEN'),
)

channel_id: str = os.getenv('UWS_SLACK_CHANNEL_ID', '')

def msg(text: str) -> bool:
	log.debug('%s: send message', channel_id)
	res = app.client.chat_postMessage(channel = channel_id, text = text)
	if not res.get('ok', False):
		log.error('%s: send message failed: %s', channel_id, res)
		return False
	return True

def main(argv: list[str]) -> int:
	if not msg(' '.join(argv)):
		return 1
	return 0

if __name__ == '__main__': # pragma: no cover
	sys.exit(main(sys.argv[1:]))
