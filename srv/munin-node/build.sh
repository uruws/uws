#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-node-2109 || true
docker rmi uws/munin-node-2203 || true
# uws/munin-node-2211
docker build --rm -t uws/munin-node-2211 \
	-f srv/munin-node/Dockerfile.2211 \
	./srv/munin-node
exit 0
