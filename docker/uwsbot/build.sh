#!/bin/sh
set -eu
mkdir -vp ./docker/uwsbot/build
cp -va ./go/etc/env/bot/default ./docker/uwsbot/build/env.default
exec docker build $@ --rm -t uws/uwsbot ./docker/uwsbot
