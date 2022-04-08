#!/bin/sh
set -eu
# acme
#docker build $@ --rm -t uws/acme \
#	-f srv/acme/Dockerfile \
#	./srv/acme
docker rmi uws/acme || true
# acme-2203
docker build $@ --rm -t uws/acme-2203 \
	-f srv/acme/Dockerfile.2203 \
	./srv/acme
exit 0
