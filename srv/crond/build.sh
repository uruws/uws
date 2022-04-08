#!/bin/sh
set -eu
# crond
#docker build --rm -t uws/crond \
#	-f srv/crond/Dockerfile \
#	./srv/crond
docker rmi uws/crond || true
# crond-2203
docker build --rm -t uws/crond-2203 \
	-f srv/crond/Dockerfile.2203 \
	./srv/crond
exit 0
