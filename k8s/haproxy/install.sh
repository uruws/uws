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
uwskube delete hpa/haproxy-ingress                    -n "${HPX_NAMESPACE}"
uwskube delete deploy/haproxy-ingress                 -n "${HPX_NAMESPACE}"

uwskube delete clusterrole/haproxy-ingress
uwskube delete clusterrolebinding/haproxy-ingress
set -e

helm upgrade --install haproxy-ingress haproxy-ingress \
	--repo https://haproxy-ingress.github.io/charts \
	--namespace "${HPX_NAMESPACE}" \
	--version "$(cat ~/k8s/haproxy/VERSION)" \
	--values "${vfn}"

rm -f "${vfn}"
exit 0
