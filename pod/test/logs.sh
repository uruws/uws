#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n uwspod \
	-l 'app.kubernetes.io/name=podtest' \
	--max 100 "$@"
