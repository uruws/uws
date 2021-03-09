#!/bin/sh
set -eu
rm -vfr ./docker/uwsbot/build/env/bot
mkdir -vp ./docker/uwsbot/build/env/bot/bot
install -C -v -m 644 ./go/etc/env/bot/* ./docker/uwsbot/build/env/bot/bot
exec docker build $@ --rm -t uws/uwsbot ./docker/uwsbot
