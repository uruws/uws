#!/bin/sh
set -eu
# munin-backend
docker build $@ --rm -t uws/munin-backend \
	-f srv/munin-backend/Dockerfile \
	./srv/munin-backend
# munin-backend-2203
docker build $@ --rm -t uws/munin-backend-2203 \
	-f srv/munin-backend/Dockerfile.2203 \
	./srv/munin-backend
exit 0
