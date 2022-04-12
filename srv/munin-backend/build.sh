#!/bin/sh
set -eu
docker rmi uws/munin-backend || true
# munin-backend-2203
docker build $@ --rm -t uws/munin-backend-2203 \
	-f srv/munin-backend/Dockerfile.2203 \
	./srv/munin-backend
exit 0
