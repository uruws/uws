#!/bin/sh
set -eu
${HOME}/pod/meteor/worker/configure.sh
exec uwskube rollout restart deployment -n worker
