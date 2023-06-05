#!/bin/sh
set -eu

# https://haproxy-ingress.github.io/docs/getting-started/

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

# shellcheck source=/home/uws/k8s/haproxy/configure.sh
. ~/k8s/haproxy/configure.sh

vfn=$(mktemp -p /tmp haproxy-${HPX_NAMESPACE}-install-XXXXXXXXXX)

haproxy_configure "${vfn}" "${prof}"

set +e
uwskube delete deploy/haproxy-ingress-default-backend -n "${HPX_NAMESPACE}"
uwskube delete hpa/haproxy-ingress                    -n "${HPX_NAMESPACE}"
uwskube delete deploy/haproxy-ingress                 -n "${HPX_NAMESPACE}"
set -e

helm upgrade --install haproxy-ingress haproxy-ingress \
	--repo https://haproxy-ingress.github.io/charts \
	--namespace "${HPX_NAMESPACE}" \
	--version 0.14.3 \
	--values "${vfn}"

rm -f "${vfn}"
exit 0
