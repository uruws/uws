#!/bin/sh
set -eu
rsync -vax --delete-before ./docker/k8s/build/ ./docker/k8s/122/build/
./docker/k8s/122/build.sh
exit 0
