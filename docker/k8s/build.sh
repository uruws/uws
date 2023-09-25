#!/bin/sh
set -eu
# remove old
# 1.22
docker rmi uws/k8s-122-2211 || true
# cleanup
# 1.24
docker rmi uws/k8s-124-2305 || true
# build
# 1.24
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/124/build/
# k8s-124-2309
docker build --rm -t uws/k8s-124-2309 \
    -f docker/k8s/124/Dockerfile.2309 \
    ./docker/k8s/124
exit 0
