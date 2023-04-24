#!/bin/sh
set -u

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

exec helm uninstall --namespace "${HPX_NAMESPACE}" haproxy-ingress
