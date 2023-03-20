#!/bin/sh
set -eu
# uws/chatbot-2211
docker build --rm -t uws/chatbot-2211 \
	-f srv/chatbot/Dockerfile.2211 \
	./srv/chatbot
exit 0
