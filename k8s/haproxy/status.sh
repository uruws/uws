#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
uwskube get all -n "${HPX_NAMESPACE}" -l 'app.kubernetes.io/name=haproxy-ingress'
exec uwskube get ingress -n "${HPX_NAMESPACE}" -l "uws.t.o/ingress-class=${HPX_NAMESPACE}hpx"
