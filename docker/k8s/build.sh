#!/bin/sh
set -eu
# 1.22
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/122/build/
# k8s-122-2211
docker build --rm -t uws/k8s-122-2211 \
    -f docker/k8s/122/Dockerfile.2211 \
    ./docker/k8s/122
# 1.25
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/125/build/
# k8s-125-2211
docker build --rm -t uws/k8s-125-2211 \
    -f docker/k8s/125/Dockerfile.2211 \
    ./docker/k8s/125
exit 0
