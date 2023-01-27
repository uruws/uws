#!/bin/sh
set -eu
# 1.22
# eks-122-2211
docker build --rm -t uws/eks-122-2211 \
    -f docker/eks/122/Dockerfile.2211 \
    ./docker/eks/122
# 1.25
# eks-125-2211
docker build --rm -t uws/eks-125-2211 \
    -f docker/eks/125/Dockerfile.2211 \
    ./docker/eks/125
exit 0
