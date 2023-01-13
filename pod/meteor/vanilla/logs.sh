#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n meteor-vanilla \
	-l 'app.kubernetes.io/name=meteor' "$@"
