#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec ~/pod/lib/logs.py -n "${HPX_NAMESPACE}" --no-timestamps \
	-l 'app.kubernetes.io/name=haproxy-ingress' \
	--max 200 -c haproxy-ingress "$@"
