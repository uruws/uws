#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-2211 || true
# uws/munin-2305
docker build --rm -t uws/munin-2305 \
	-f srv/munin/Dockerfile.2305 \
	./srv/munin
exit 0
