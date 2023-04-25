#!/bin/sh
set -eu

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

uwskube create namespace "${HPX_NAMESPACE}"
exec ~/k8s/haproxy/install.sh "${prof}"
