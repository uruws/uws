#!/bin/sh
set -eu
prof=${1:?'haproxy profile?'}
replicas=${2:?'haproxy replicas?'}
shift
shift
envfn="${HOME}/${prof}/haproxy.env"
# shellcheck disable=SC1090
. "${envfn}"
exec ~/pod/lib/scale.sh "${HPX_NAMESPACE}" haproxy-ingress "${replicas}"
