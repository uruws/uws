#!/bin/sh
set -eu
~/k8s/mon/munin/configure.sh
exec uwskube rollout restart deployment "${UWS_CLUSTER}-munin" -n mon
