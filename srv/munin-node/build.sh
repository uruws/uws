#!/bin/sh
set -eu
mkdir -vp ./srv/munin-node/build
cp -va ./go/etc/munin/plugin-conf.d/uwsbot ./srv/munin-node/build/uwsbot-plugin.conf
exec docker build $@ --rm -t uws/munin-node ./srv/munin-node
