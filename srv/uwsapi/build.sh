#!/bin/sh
set -eu
# api-2203
docker build --rm -t uws/api-2203 \
	-f srv/uwsapi/Dockerfile.2203 \
	./srv/uwsapi
exit 0
