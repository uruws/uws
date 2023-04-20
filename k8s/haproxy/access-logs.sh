#!/bin/sh
set -eu
ns=${1:?'haproxy namespace?'}
shift
exec ~/pod/lib/logs.py -n "${ns}" --no-timestamps \
	-l 'app.kubernetes.io/name=haproxy-ingress' \
	--max 200 -c access-logs "$@"
