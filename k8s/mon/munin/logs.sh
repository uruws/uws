#!/bin/sh
set -eu
exec ~/pod/lib/logs.py -n mon -c ${UWS_CLUSTER}-munin deployment/munin "$@"
