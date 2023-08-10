#!/bin/sh
set -eu
# uws/admin-2305
docker build --rm -t uws/admin-2305 \
	-f srv/admin/Dockerfile.2305 \
	./srv/admin
exit 0
