#!/bin/sh
set -eu

rm -vfr ./docker/uwsbot/build/env/bot
mkdir -vp ./docker/uwsbot/build/env/bot/bot
install -C -v -m 644 ./go/etc/env/bot/* ./docker/uwsbot/build/env/bot/bot

docker rmi uws/uwsbot || true

# uwsbot-2203
docker build --rm -t uws/uwsbot-2203 \
	-f docker/uwsbot/Dockerfile.2203 \
	./docker/uwsbot

exit 0
