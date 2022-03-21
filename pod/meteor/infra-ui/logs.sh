#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n infra-ui-${INFRA_UI_ENV} \
	-l 'app.kubernetes.io/name=meteor' \
	--max 100 "$@"
