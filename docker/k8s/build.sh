#!/bin/sh
set -eu
# remove old
# 1.25
docker rmi uws/k8s-125-2211 || true
# build
# 1.22
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/122/build/
# k8s-122-2211
docker build --rm -t uws/k8s-122-2211 \
    -f docker/k8s/122/Dockerfile.2211 \
    ./docker/k8s/122
exit 0
