#!/bin/sh
set -eu
# remove old versions
docker rmi uws/nginx-2211 || true
# uws/nginx-2305
docker build --rm -t uws/nginx-2305 \
	-f srv/nginx/Dockerfile.2305 \
	./srv/nginx
# uws/nginx-2309
docker build --rm -t uws/nginx-2309 \
	-f srv/nginx/Dockerfile.2309 \
	./srv/nginx
exit 0
