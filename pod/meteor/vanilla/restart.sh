#!/bin/sh
set -eu
${HOME}/pod/meteor/vanilla/configure.sh
exec uwskube rollout restart deployment -n meteor-vanilla
