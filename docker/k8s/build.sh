#!/bin/sh
set -eu
docker build --rm -t uws/k8s ./docker/k8s
docker build --rm -t uws/k8s:devel \
	-f ./docker/k8s/Dockerfile.devel ./docker/k8s
exit 0
