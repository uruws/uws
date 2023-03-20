#!/bin/sh
set -eu
# uws/ab-2211
docker build --rm -t uws/ab-2211 \
	-f srv/ab/Dockerfile.2211 \
	./srv/ab
exit 0
