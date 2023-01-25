#!/bin/sh
set -eu
# k8s-122
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/122/build/
./docker/k8s/122/build.sh
# k8s-125
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/125/build/
./docker/k8s/125/build.sh
exit 0
