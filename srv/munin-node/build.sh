#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-node-2211 || true
docker rmi uws/munin-node-2305 || true
# uws/munin-node-2309
docker build --rm -t uws/munin-node-2309 \
	-f srv/munin-node/Dockerfile.2309 \
	./srv/munin-node
exit 0
