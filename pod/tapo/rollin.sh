#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
exec uwskube delete "deployment/meteor-${app}" -n "${ns}"
