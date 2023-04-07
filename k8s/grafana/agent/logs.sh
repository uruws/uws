#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n grfn --max 100 \
	-l app.kubernetes.io/name=grafana-agent --all-containers "$@"
