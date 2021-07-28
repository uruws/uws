#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n worker -l 'app.kubernetes.io/name=meteor-worker' --max 600 $@
