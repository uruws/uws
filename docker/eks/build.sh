#!/bin/sh
set -eu
# remove old
# 125
docker rmi uws/eks-125-2211 || true
# build
# 122
# eks-122-2211
docker build --rm -t uws/eks-122-2211 \
    -f docker/eks/122/Dockerfile.2211 \
    ./docker/eks/122
# 124
# eks-124-2211
docker build --rm -t uws/eks-124-2211 \
    -f docker/eks/124/Dockerfile.2211 \
    ./docker/eks/124
exit 0
