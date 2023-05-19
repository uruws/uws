#!/bin/sh
set -eu
# remove old versions
docker rmi uws/nginx-2203 || true
# uws/nginx-2211
docker build --rm -t uws/nginx-2211 \
	-f srv/nginx/Dockerfile.2211 \
	./srv/nginx
# uws/nginx-2305
docker build --rm -t uws/nginx-2305 \
	-f srv/nginx/Dockerfile.2305 \
	./srv/nginx
exit 0
