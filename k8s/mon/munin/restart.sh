#!/bin/sh
set -eu
~/k8s/mon/munin/configure.sh
exec uwskube rollout restart sts munin -n mon
