#!/bin/sh
set -eu
${HOME}/pod/meteor/web/configure.sh
exec uwskube rollout restart deployment -n web
