#!/bin/sh
set -eu
# remove old versions
docker rmi uws/mailx-2203 || true
docker rmi uws/mailx-2211 || true
# uws/mailx-2305
docker build --rm -t uws/mailx-2305 \
	-f docker/mailx/Dockerfile.2305 \
	./docker/mailx
exit 0
