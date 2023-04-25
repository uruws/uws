#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec ~/pod/lib/top.sh "${HPX_NAMESPACE}" -l 'app.kubernetes.io/name=haproxy-ingress' --containers=true
