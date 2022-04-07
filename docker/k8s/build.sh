#!/bin/sh
set -eu
# k8s
#docker build --rm -t uws/k8s \
#	-f docker/k8s/Dockerfile \
#	./docker/k8s
docker rmi uws/k8s || true
# k8s-2203
docker build --rm -t uws/k8s-2203 \
	-f docker/k8s/Dockerfile.2203 \
	./docker/k8s
exit 0
