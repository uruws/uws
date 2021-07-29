#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n web -l 'app.kubernetes.io/name=meteor-web' --max 300 $@
