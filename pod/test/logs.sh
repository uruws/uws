#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n default \
	-l 'app.kubernetes.io/name=podtest' \
	"$@"
