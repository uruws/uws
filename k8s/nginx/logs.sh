#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n nginx \
	-l 'app.kubernetes.io/name=proxy' \
	"$@"
