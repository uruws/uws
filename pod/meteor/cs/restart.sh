#!/bin/sh
set -eu
~/pod/meteor/cs/configure.sh "${METEOR_CS_ENV}"
uwskube rollout restart deployment -n cs
~/pod/meteor/cs/gw/restart.sh
exit 0
