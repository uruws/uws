#!/bin/sh
set -eu

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

#uwskube create namespace "${HPX_NAMESPACE}"
exit 0
