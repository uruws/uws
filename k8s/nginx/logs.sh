#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n nginx --no-timestamps \
	-l 'app.kubernetes.io/name=proxy' \
	"$@"
