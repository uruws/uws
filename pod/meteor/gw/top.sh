#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec ~/k8s/nginx/top.sh "${ns}"
