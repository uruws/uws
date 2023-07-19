#!/bin/sh
set -eu

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/ca-setup.sh "${HPX_NAMESPACE}"

exit 0
