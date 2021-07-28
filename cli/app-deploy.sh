#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
kind=${2:?'kind?'}
release=${3:?'release?'}
cd /srv/uws/deploy
exec ./docker/k8s/cli.sh ${cluster} ./pod/${kind}/deploy.sh "${release}"
