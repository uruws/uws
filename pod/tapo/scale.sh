#!/bin/sh
set -eu
ns=${1:?'namespace?'}
app=${2:?'app name?'}
replicas=${3:?'app replicas?'}
exec ~/pod/lib/scale.sh "${ns}" "meteor-${app}" "${replicas}"
