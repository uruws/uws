# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import logging
import sys

from pathlib import Path

# local conf

conf = Path('/etc/opt/uws/chatbot/chatbot_conf.py')
if conf.exists() and conf.is_file() and not conf.is_symlink():
	sys.path.insert(0, conf.parent.as_posix())
	import chatbot_conf # type: ignore

import chatbot
import chatbot_slack

#
# views
#

@bottle.post('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return 'OK'
	raise RuntimeError('slack chatbot not healthy')

#
# main
#

def start():
	logging.debug('start')
	chatbot_slack.connect()
	logging.debug('slack connected')
	chatbot_slack.msg('connected')

def getapp():
	start()
	return bottle.app

def main():
	start()
	logging.debug('bottle run')
	bottle.run(
		host     = '0.0.0.0',
		port     = chatbot.webapp_port,
		reloader = True,
		debug    = True,
	)

if __name__ == '__main__': # pragma: no cover
	if chatbot.debug:
		logging.basicConfig(level = logging.DEBUG)
	main()
