#!/bin/sh
set -eu

envfn=${1:?'haproxy env file?'}

# shellcheck disable=SC1090
. "${envfn}"

uwskube create namespace "${HPX_NAMESPACE}"
exec ~/k8s/haproxy/install.sh "${envfn}"
