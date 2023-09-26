#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-backend-2211 || true
docker rmi uws/munin-backend-2305 || true
# uws/munin-backend-2309
docker build --rm -t uws/munin-backend-2309 \
	-f srv/munin-backend/Dockerfile.2309 \
	./srv/munin-backend
exit 0
