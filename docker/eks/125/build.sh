#!/bin/sh
set -eu
# uws/eks-125-2211
docker build --rm -t uws/eks-125-2211 \
	-f docker/eks/125/Dockerfile.2211 \
	./docker/eks/125
exit 0
