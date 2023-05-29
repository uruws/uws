#!/bin/sh
set -eu
~/pod/meteor/web/configure.sh
exec uwskube rollout restart deployment -n web
