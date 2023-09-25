#!/bin/sh
set -eu
# remove old
# 1.22
docker rmi uws/eks-122-2211 || true
# cleanup
# 1.24
docker rmi uws/eks-124-2305 || true
# build
# 1.24
# eks-124-2309
docker build --rm -t uws/eks-124-2309 \
    -f docker/eks/124/Dockerfile.2309 \
    ./docker/eks/124
exit 0
