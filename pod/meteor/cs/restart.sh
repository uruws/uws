#!/bin/sh
set -eu
~/pod/meteor/cs/configure.sh "${METEOR_CS_ENV}"
exec uwskube rollout restart deployment -n cs
