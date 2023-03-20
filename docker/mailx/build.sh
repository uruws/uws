#!/bin/sh
set -eu
# remove old versions
docker rmi uws/mailx-2109 || true
# uws/mailx-2203
docker build --rm -t uws/mailx-2203 \
	-f docker/mailx/Dockerfile.2203 \
	./docker/mailx
# uws/mailx-2211
docker build --rm -t uws/mailx-2211 \
	-f docker/mailx/Dockerfile.2211 \
	./docker/mailx
exit 0
