#!/bin/sh
set -eu

VERSION='0.6.4'
SRCD=${PWD}/../metrics-server

git -C "${SRCD}" fetch --all
git -C "${SRCD}" checkout v${VERSION}

rsync -vax --delete-before "${SRCD}/manifests/base/" ./k8s/metrics-server/deploy/base/
rsync -vax --delete-before "${SRCD}/manifests/release/" ./k8s/metrics-server/deploy/release/

exit 0
