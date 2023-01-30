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
# 1.24
# eks-124-2211
docker build --rm -t uws/eks-124-2211 \
    -f docker/eks/124/Dockerfile.2211 \
    ./docker/eks/124
exit 0
