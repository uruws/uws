#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin pod/${UWS_CLUSTER}-munin-0 "$@"
