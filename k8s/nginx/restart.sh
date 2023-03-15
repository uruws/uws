#!/bin/sh
set -eu
ns=${1:?'namespace?'}
gw=${2:?'gateway?'}
~/k8s/nginx/configure.sh "${ns}" "${gw}"
exec uwskube rollout restart deployment proxy -n "${ns}"
