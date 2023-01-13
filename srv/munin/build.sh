#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-2109 || true
# uws/munin-2203
docker build --rm -t uws/munin-2203 \
	-f srv/munin/Dockerfile.2203 \
	./srv/munin
# uws/munin-2211
docker build --rm -t uws/munin-2211 \
	-f srv/munin/Dockerfile.2211 \
	./srv/munin
exit 0
