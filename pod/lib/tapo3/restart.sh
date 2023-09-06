#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
~/pod/lib/tapo3/configure.sh "${ns}" "${app}"
~/pod/lib/tapo3/ngx/configure.sh "${ns}" "${app}"
exec uwskube rollout restart "deployment/meteor-${app}" -n "${ns}"
