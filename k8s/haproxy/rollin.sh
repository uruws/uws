#!/bin/sh
set -eu

envfn=${1:?'haproxy env file?'}
ingfn=${2:?'haproxy ingress file?'}

# shellcheck disable=SC1090
. "${envfn}"

# shellcheck source=/home/uws/k8s/haproxy/ingress-configure.sh
. ~/k8s/haproxy/ingress-configure.sh

ifn=$(mktemp -p /tmp haproxy-${HPX_NAMESPACE}-ingress-rollin-XXXXXXXXXX)

haproxy_ingress_configure "${ifn}" "${envfn}" "${ingfn}"

uwskube delete -n "${HPX_NAMESPACE}" -f "${ifn}"

rm -f "${ifn}"
exit 0
