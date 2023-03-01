#!/bin/sh
set -eu
ns="${1:?'namespace?'}gw"
exec ~/k8s/nginx/logs.sh "${ns}" "$@"
