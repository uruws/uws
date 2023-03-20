#!/bin/sh
set -eu
ns=${1:?'namespace?'}
shift
exec ~/pod/lib/logs.py -n "${ns}" --no-timestamps \
	-l 'app.kubernetes.io/name=proxy' \
	--max 100 \
	"$@"
