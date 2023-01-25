#!/bin/sh
set -eu
# uws/k8s-125-2211
docker build --rm -t uws/k8s-125-2211 \
	-f docker/k8s/125/Dockerfile.2211 \
	./docker/k8s/125
exit 0
