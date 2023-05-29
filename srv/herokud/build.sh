#!/bin/sh
set -eu
# remove old versions
docker rmi uws/herokud-2203 || true
# uws/herokud-2211
docker build --rm -t uws/herokud-2211 \
	-f srv/herokud/Dockerfile.2211 \
	./srv/herokud
# uws/herokud-2305
docker build --rm -t uws/herokud-2305 \
	-f srv/herokud/Dockerfile.2305 \
	./srv/herokud
exit 0
