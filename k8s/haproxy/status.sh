#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec uwskube get all -n "${HPX_NAMESPACE}" -l 'app.kubernetes.io/name=haproxy-ingress'
