#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n nlpsvc --max 100 \
	-l 'app.kubernetes.io/name=sentiment-twitter' \
	"$@"
