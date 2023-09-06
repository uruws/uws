#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
shift
shift
exec ~/pod/lib/logs.py -n "${ns}" -c "meteor-${app}" \
	-l "app.kubernetes.io/name=meteor-${app}" "$@"
