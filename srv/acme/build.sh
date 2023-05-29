#!/bin/sh
set -eu
# remove old versions
docker rmi uws/acme-2203 || true
# uws/acme-2211
docker build --rm -t uws/acme-2211 \
	-f srv/acme/Dockerfile.2211 \
	./srv/acme
# uws/acme-2305
docker build --rm -t uws/acme-2305 \
	-f srv/acme/Dockerfile.2305 \
	./srv/acme
exit 0
