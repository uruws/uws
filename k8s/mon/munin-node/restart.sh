#!/bin/sh
set -eu
~/k8s/mon/munin-node/configure.sh
exec uwskube rollout restart deploy munin-node -n mon
