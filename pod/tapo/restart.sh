#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
exec uwskube rollout restart "deployment/meteor-${app}" -n "${ns}"
