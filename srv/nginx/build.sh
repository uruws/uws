#!/bin/sh
set -eu
# uws/nginx-2211
docker build --rm -t uws/nginx-2211 \
	-f srv/nginx/Dockerfile.2211 \
	./srv/nginx
exit 0
