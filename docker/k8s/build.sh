#!/bin/sh
set -eu
docker build --rm -t uws/k8s ./docker/k8s
exit 0
