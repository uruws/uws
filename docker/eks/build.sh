#!/bin/sh
set -eu
# remove old
# 1.22
docker rmi uws/eks-122-2211 || true
# build
# 1.24
# eks-124-2305
docker build --rm -t uws/eks-124-2305 \
    -f docker/eks/124/Dockerfile.2305 \
    ./docker/eks/124
exit 0
