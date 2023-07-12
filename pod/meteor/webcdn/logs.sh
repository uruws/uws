#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n webcdn \
	-l 'app.kubernetes.io/name=meteor-webcdn' \
	--max 200 "$@"
