#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n netdata -l 'role=k8sState' "$@"
