#!/bin/sh
set -eu
# remove old versions
docker rmi uws/herokud-2211 || true
# uws/herokud-2305
docker build --rm -t uws/herokud-2305 \
	-f srv/herokud/Dockerfile.2305 \
	./srv/herokud
exit 0
