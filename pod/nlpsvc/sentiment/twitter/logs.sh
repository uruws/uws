#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n nlpsvc \
	-l 'app.kubernetes.io/name=sentiment-twitter' \
	"$@"
