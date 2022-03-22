#!/bin/sh
set -eu
# mailx
docker build --rm -t uws/mailx \
	-f docker/mailx/Dockerfile \
	./docker/mailx
# mailx-2203
docker build --rm -t uws/mailx-2203 \
	-f docker/mailx/Dockerfile.2203 \
	./docker/mailx
exit 0
