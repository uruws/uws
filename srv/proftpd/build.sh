#!/bin/sh
set -eu
# remove old versions
docker rmi uws/proftpd-2109 || true
# uws/proftpd-2203
docker build --rm -t uws/proftpd-2203 \
	-f srv/proftpd/Dockerfile.2203 \
	./srv/proftpd
# uws/proftpd-2211
docker build --rm -t uws/proftpd-2211 \
	-f srv/proftpd/Dockerfile.2211 \
	./srv/proftpd
exit 0
