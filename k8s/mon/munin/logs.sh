#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c munin deployment/${UWS_CLUSTER}-munin "$@"
