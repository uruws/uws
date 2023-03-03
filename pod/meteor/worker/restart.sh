#!/bin/sh
set -eu
~/pod/meteor/worker/configure.sh
uwskube rollout restart deployment -n worker
~/pod/meteor/worker/gw/restart.sh
exit 0
