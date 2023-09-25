#!/bin/sh
set -eu
# remove old versions
docker rmi uws/admin-2211 || true
# uws/admin-2305
docker build --rm -t uws/admin-2305 \
	-f srv/admin/Dockerfile.2305 \
	./srv/admin
# uws/admin-2309
docker build --rm -t uws/admin-2309 \
	-f srv/admin/Dockerfile.2309 \
	./srv/admin
exit 0
