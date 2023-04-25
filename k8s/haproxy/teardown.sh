#!/bin/sh
set -u

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/uninstall.sh "${prof}"
exec uwskube delete namespace "${HPX_NAMESPACE}"
