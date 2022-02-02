#!/bin/sh
set -eu
${HOME}/pod/meteor/beta/configure.sh
exec uwskube rollout restart deployment -n meteor-beta
