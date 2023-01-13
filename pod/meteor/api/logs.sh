#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n api \
	-l 'app.kubernetes.io/name=meteor-api' \
	--max 200 "$@"
