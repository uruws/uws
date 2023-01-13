#!/bin/sh
set -eu
${HOME}/pod/meteor/api/configure.sh
exec uwskube rollout restart deployment -n api
