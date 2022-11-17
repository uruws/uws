#!/bin/sh
set -eu
# remove old versions
docker rmi uws/crond-2109 || true
# uws/crond-2203
docker build --rm -t uws/crond-2203 \
	-f srv/crond/Dockerfile.2203 \
	./srv/crond
# uws/crond-2211
docker build --rm -t uws/crond-2211 \
	-f srv/crond/Dockerfile.2211 \
	./srv/crond
exit 0
