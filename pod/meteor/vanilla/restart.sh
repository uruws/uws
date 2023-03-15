#!/bin/sh
set -eu
~/pod/meteor/vanilla/configure.sh
uwskube rollout restart deployment -n meteor-vanilla
~/pod/meteor/vanilla/gw/restart.sh
exit 0
