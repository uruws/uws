#!/bin/sh
set -eu
# remove old versions
docker rmi uws/uwsbot-2109 || true
# uws/uwsbot-2203
docker build --rm -t uws/uwsbot-2203 \
	-f docker/uwsbot/Dockerfile.2203 \
	./docker/uwsbot
# uws/uwsbot-2211
docker build --rm -t uws/uwsbot-2211 \
	-f docker/uwsbot/Dockerfile.2211 \
	./docker/uwsbot
exit 0
