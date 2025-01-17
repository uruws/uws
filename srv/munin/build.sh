#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-2211 || true
docker rmi uws/munin-2305 || true
# uws/munin-2309
docker build --rm -t uws/munin-2309 \
	-f srv/munin/Dockerfile.2309 \
	./srv/munin
exit 0
