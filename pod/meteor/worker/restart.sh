#!/bin/sh
set -eu
~/pod/meteor/worker/configure.sh
exec uwskube rollout restart deployment -n worker
