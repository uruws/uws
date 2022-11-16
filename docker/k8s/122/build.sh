#!/bin/sh
set -eu
# remove old versions
docker rmi uws/k8s-122-2109 || true
# uws/k8s-122-2203
docker build --rm -t uws/k8s-122-2203 \
	-f docker/k8s/122/Dockerfile.2203 \
	./docker/k8s/122
# uws/k8s-122-2211
docker build --rm -t uws/k8s-122-2211 \
	-f docker/k8s/122/Dockerfile.2211 \
	./docker/k8s/122
exit 0
