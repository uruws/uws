#!/bin/sh
set -eu
export K8S_DEVEL_LOGIN='true'
exec ./docker/k8s/devel.sh
