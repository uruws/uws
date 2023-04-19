#!/bin/sh
set -u

envfn=${1:?'haproxy env file?'}

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/uninstall.sh "${envfn}"
exec uwskube delete namespace "${HPX_NAMESPACE}hpx"
