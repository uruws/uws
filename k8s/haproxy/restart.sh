#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec uwskube rollout restart "deployment/${HPX_NAME}-haproxy-ingress" -n "${HPX_NAMESPACE}"
