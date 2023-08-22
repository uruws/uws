#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns=${TAPO_NAMESPACE}
exec ~/pod/tapo/ngx/scale.sh "${ns}" "${replicas}"
