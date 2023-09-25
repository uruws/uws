#!/bin/sh
set -eu
# remove old versions
docker rmi uws/crond-2211 || true
# uws/crond-2305
docker build --rm -t uws/crond-2305 \
	-f srv/crond/Dockerfile.2305 \
	./srv/crond
# uws/crond-2309
docker build --rm -t uws/crond-2309 \
	-f srv/crond/Dockerfile.2309 \
	./srv/crond
exit 0
