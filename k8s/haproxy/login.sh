#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec uwskube exec deploy/haproxy-ingress -n "${HPX_NAMESPACE}" -it -c haproxy-ingress -- /bin/sh -il
