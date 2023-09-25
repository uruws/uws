#!/bin/sh
set -eu
# remove old versions
docker rmi uws/ab-2211 || true
# uws/ab-2305
docker build --rm -t uws/ab-2305 \
	-f srv/ab/Dockerfile.2305 \
	./srv/ab
# uws/ab-2309
docker build --rm -t uws/ab-2309 \
	-f srv/ab/Dockerfile.2309 \
	./srv/ab
exit 0
