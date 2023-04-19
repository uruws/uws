#!/bin/sh
set -u

envfn=${1:?'haproxy env file?'}

# shellcheck disable=SC1090
. "${envfn}"

exec helm uninstall --namespace "${HPX_NAMESPACE}hpx" haproxy-ingress
