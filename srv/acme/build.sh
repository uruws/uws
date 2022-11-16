#!/bin/sh
set -eu
# remove old versions
docker rmi uws/acme-2109 || true
# uws/acme-2203
docker build --rm -t uws/acme-2203 \
	-f srv/acme/Dockerfile.2203 \
	./srv/acme
# uws/acme-2211
docker build --rm -t uws/acme-2211 \
	-f srv/acme/Dockerfile.2211 \
	./srv/acme
exit 0
