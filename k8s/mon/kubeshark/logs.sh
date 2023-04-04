#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n kubeshark -l 'app.kubernetes.io/name=worker' "$@"
