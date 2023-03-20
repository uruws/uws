#!/bin/sh
set -eu
~/pod/meteor/web/configure.sh
uwskube rollout restart deployment -n web
~/pod/meteor/web/gw/restart.sh
exit 0
