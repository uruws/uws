#!/bin/sh
set -eu
VERSION='0.5.1'
SRCD=../../../metrics-server

wd=${PWD}
cd ${SRCD}/

git fetch --all
git checkout v${VERSION}

cd ${wd}
rsync -vax --delete-before ${SRCD}/manifests/base/ ./deploy/base/
rsync -vax --delete-before ${SRCD}/manifests/release/ ./deploy/release/

exit 0
