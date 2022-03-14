#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n infra-ui \
	-l 'app.kubernetes.io/name=meteor' \
	--max 100 "$@"
