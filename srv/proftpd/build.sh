#!/bin/sh
set -eu
# remove old versions
docker rmi uws/proftpd-2203 || true
# uws/proftpd-2211
docker build --rm -t uws/proftpd-2211 \
	-f srv/proftpd/Dockerfile.2211 \
	./srv/proftpd
# uws/proftpd-2305
docker build --rm -t uws/proftpd-2305 \
	-f srv/proftpd/Dockerfile.2305 \
	./srv/proftpd
exit 0
