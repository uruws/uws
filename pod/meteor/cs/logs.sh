#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n cs -l 'app.kubernetes.io/name=meteor' --max 100 $@
