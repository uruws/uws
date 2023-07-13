#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
~/pod/tapo/configure.sh "${ns}" "${app}"
exec uwskube rollout restart "deployment/meteor-${app}" -n "${ns}"
