#!/bin/sh
set -eu
# remove old
# 1.25
docker rmi uws/eks-125-2211 || true
# build
# 1.22
# eks-122-2211
docker build --rm -t uws/eks-122-2211 \
    -f docker/eks/122/Dockerfile.2211 \
    ./docker/eks/122
exit 0
