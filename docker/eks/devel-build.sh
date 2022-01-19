#!/bin/sh
set -eu
docker build --rm -t uws/eks:devel \
	-f docker/eks/Dockerfile.devel \
	./docker/eks
exit 0
