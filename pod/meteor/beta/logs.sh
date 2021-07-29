#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n meteor-beta -l 'app.kubernetes.io/name=meteor-beta' --max 100 $@
