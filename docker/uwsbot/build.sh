#!/bin/sh
set -eu
rm -vfr ./docker/uwsbot/build/env/bot
mkdir -vp ./docker/uwsbot/build/env/bot
cp -va ./go/etc/env/bot ./docker/uwsbot/build/env/bot
exec docker build $@ --rm -t uws/uwsbot ./docker/uwsbot
