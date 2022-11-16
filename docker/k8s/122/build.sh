#!/bin/sh
set -eu
docker rmi uws/k8s || true
# k8s-2203
docker build --rm -t uws/k8s-2203 \
	-f docker/k8s/Dockerfile.2203 \
	./docker/k8s
# k8s-122-2203
docker build --rm -t uws/k8s-122-2203 \
	-f docker/k8s/Dockerfile-122.2203 \
	./docker/k8s
exit 0
