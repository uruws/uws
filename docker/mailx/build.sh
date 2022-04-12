#!/bin/sh
set -eu
docker rmi uws/mailx || true
# mailx-2203
docker build --rm -t uws/mailx-2203 \
	-f docker/mailx/Dockerfile.2203 \
	./docker/mailx
exit 0
