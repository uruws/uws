#!/bin/sh
set -eu
# remove old versions
docker rmi uws/eks-122-2109 || true
# uws/eks-122-2203
docker build --rm -t uws/eks-122-2203 \
	-f docker/eks/122/Dockerfile.2203 \
	./docker/eks/122
# uws/eks-122-2211
docker build --rm -t uws/eks-122-2211 \
	-f docker/eks/122/Dockerfile.2211 \
	./docker/eks/122
exit 0
