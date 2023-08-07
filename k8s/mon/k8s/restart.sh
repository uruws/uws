#!/bin/sh
set -eu
~/k8s/mon/k8s/configure.sh
exec uwskube rollout restart deploy k8s -n mon
