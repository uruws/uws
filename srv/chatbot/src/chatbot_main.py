# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import sys

from pathlib import Path

import wapp

import chatbot_conf

import chatbot
import chatbot_slack

app: wapp.Bottle = wapp.Bottle()
log: wapp.Logger = wapp.getLogger(__name__)

#
# views
#

# /healthz

@app.get('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return wapp.text_plain('ok')
	raise RuntimeError('slack chatbot not healthy')

# /send

@app.get('/send')
def send():
	return wapp.template('chatbot/send.html')

@app.post('/send')
def do_send():
	return wapp.template('chatbot/sent.html')

#
# main
#

def start():
	wapp.start(app)
	log.debug('start')
	chatbot_slack.connect()
	log.debug('slack connected')
	chatbot_slack.msg('connected')

def wsgi_application():
	start()
	log.debug('wsgi application')
	return app

def main():
	start()
	log.debug('bottle run')
	wapp.run(app)

if __name__ == '__main__': # pragma: no cover
	main()
