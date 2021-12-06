#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -T -n mon -l 'app.kubernetes.io/name=k8s' "$@"
