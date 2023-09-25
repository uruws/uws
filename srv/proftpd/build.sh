#!/bin/sh
set -eu
# remove old versions
docker rmi uws/proftpd-2211 || true
# uws/proftpd-2305
docker build --rm -t uws/proftpd-2305 \
	-f srv/proftpd/Dockerfile.2305 \
	./srv/proftpd
# uws/proftpd-2309
docker build --rm -t uws/proftpd-2309 \
	-f srv/proftpd/Dockerfile.2309 \
	./srv/proftpd
exit 0
