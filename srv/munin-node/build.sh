#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-node-2211 || true
# uws/munin-node-2305
docker build --rm -t uws/munin-node-2305 \
	-f srv/munin-node/Dockerfile.2305 \
	./srv/munin-node
# uws/munin-node-2309
docker build --rm -t uws/munin-node-2309 \
	-f srv/munin-node/Dockerfile.2309 \
	./srv/munin-node
exit 0
