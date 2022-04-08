#!/bin/sh
set -eu

mkdir -vp ./srv/munin-node/build
install -C -v -m 644 ./go/etc/env/bot/stats ./srv/munin-node/build/uwsbot-stats.env
install -C -v -m 644 ./go/etc/munin/plugin-conf.d/uwsbot ./srv/munin-node/build/uwsbot-plugin.conf

# munin-node
#docker build $@ --rm -t uws/munin-node \
#	-f srv/munin-node/Dockerfile \
#	./srv/munin-node
docker rmi uws/munin-node || true
# munin-node-2203
docker build $@ --rm -t uws/munin-node-2203 \
	-f srv/munin-node/Dockerfile.2203 \
	./srv/munin-node

exit 0
