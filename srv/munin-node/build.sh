#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-node-2109 || true
# uws/munin-node-2203
docker build --rm -t uws/munin-node-2203 \
	-f srv/munin-node/Dockerfile.2203 \
	./srv/munin-node
# uws/munin-node-2211
docker build --rm -t uws/munin-node-2211 \
	-f srv/munin-node/Dockerfile.2211 \
	./srv/munin-node
exit 0
