#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
shift
shift
ngxv=$(cat ~/k8s/nginx/VERSION)
exec ~/pod/lib/logs.py -n "${ns}" -c "ngx${ngxv}" \
	-l "app.kubernetes.io/name=meteor-${app}" "$@"
