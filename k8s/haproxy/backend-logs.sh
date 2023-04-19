#!/bin/sh
set -eu
ns="${1:?'haproxy namespace?'}hpx"
shift
exec ~/pod/lib/logs.py -n "${ns}" \
	-l 'app.kubernetes.io/name=haproxy-ingress-default-backend' \
	--max 200 "$@"
