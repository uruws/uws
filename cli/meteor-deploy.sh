#!/bin/sh
set -eu
cluster=${1:?'cluster?'}
kind=${2:?'web, worker, beta, cs?'}
release=${3:?'app release?'}
cd /srv/uws/deploy
exec ./docker/k8s/cli.sh ${cluster} ./pod/meteor/${kind}/deploy.sh "${release}"
