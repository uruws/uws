# Copyright (c) Jeremías Casteglione <jeremias@talkingpts.org>
# See LICENSE file.

import bottle # type: ignore
import sys

from pathlib import Path

import wapp

import chatbot_conf

import chatbot
import chatbot_slack

app = bottle.Bottle()
log = wapp.getLogger(__name__)

#
# views
#

# /healthz

@app.get('/healthz')
def healthz():
	if chatbot_slack.is_healthy():
		return 'ok'
	raise RuntimeError('slack chatbot not healthy')

# /send

@app.get('/send')
def send():
	return """<!DOCTYPE html>
<html>
<head>
  <title>chatbot - send</title>
</head>
<body>
  <form action="/send" method="post">
    <input type="text" name="message" required="required" placeholder="message">
    <input type="submit" name="send" value="send">
  </form>
</body>
</html>
"""

@app.post('/send')
def do_send():
	return """<!DOCTYPE html>
<html>
<head>
  <title>chatbot - message</title>
</head>
<body>
  <p>sent</p>
</body>
</html>
"""

#
# main
#

def start():
	wapp.start(chatbot.debug)
	log.debug('start')
	chatbot_slack.connect()
	log.debug('slack connected')
	chatbot_slack.msg('connected')

def wsgi_application():
	start()
	log.debug('wsgi application: %s', type(app))
	return app

def main():
	start()
	log.debug('bottle run')
	app.run(
		host     = '0.0.0.0',
		port     = chatbot.webapp_port,
		reloader = chatbot.debug,
		debug    = chatbot.debug,
	)

if __name__ == '__main__': # pragma: no cover
	main()
