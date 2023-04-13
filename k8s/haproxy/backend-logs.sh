#!/bin/sh
set -eu
ns=${1:?'haproxy namespace?'}
shift
exec ~/pod/lib/logs.py -n "${ns}" \
	-l 'app.kubernetes.io/name=haproxy-ingress-haproxy-backend' \
	--max 200 "$@"
