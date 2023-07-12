#!/bin/sh
set -eu
# remove old versions
docker rmi uws/chatbot-2203 || true
# uws/chatbot-2211
docker build --rm -t uws/chatbot-2211 \
	-f srv/chatbot/Dockerfile.2211 \
	./srv/chatbot
# uws/chatbot-2305
docker build --rm -t uws/chatbot-2305 \
	-f srv/chatbot/Dockerfile.2305 \
	./srv/chatbot
exit 0
