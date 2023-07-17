#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin-web deployment/${UWS_CLUSTER}-munin "$@"
