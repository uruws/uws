#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n grfn \
	-l app.kubernetes.io/name=kube-state-metrics "$@"
