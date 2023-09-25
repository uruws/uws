#!/bin/sh
set -eu
# remove old versions
docker rmi uws/uwsbot-2211 || true
# uws/uwsbot-2305
docker build --rm -t uws/uwsbot-2305 \
	-f docker/uwsbot/Dockerfile.2305 \
	./docker/uwsbot
# uws/uwsbot-2309
docker build --rm -t uws/uwsbot-2309 \
	-f docker/uwsbot/Dockerfile.2309 \
	./docker/uwsbot
exit 0
