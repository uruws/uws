#!/bin/sh
set -eu
~/pod/meteor/api/configure.sh
exec uwskube rollout restart deployment -n api
