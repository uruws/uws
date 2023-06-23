#!/bin/sh
set -eu
# remove old versions
docker rmi uws/munin-backend-2211 || true
# uws/munin-backend-2305
docker build --rm -t uws/munin-backend-2305 \
	-f srv/munin-backend/Dockerfile.2305 \
	./srv/munin-backend
exit 0
