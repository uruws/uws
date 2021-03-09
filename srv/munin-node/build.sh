#!/bin/sh
set -eu
mkdir -vp ./srv/munin-node/build
install -C -v -m 644 ./go/etc/env/bot/stats ./srv/munin-node/build/uwsbot-stats.env
install -C -v -m 644 ./go/etc/munin/plugin-conf.d/uwsbot ./srv/munin-node/build/uwsbot-plugin.conf
exec docker build $@ --rm -t uws/munin-node ./srv/munin-node
