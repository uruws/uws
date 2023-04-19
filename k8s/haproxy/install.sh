#!/bin/sh
set -eu

# https://haproxy-ingress.github.io/docs/getting-started/

envfn=${1:?'haproxy env file?'}

# shellcheck disable=SC1090
. "${envfn}"

# shellcheck source=/home/uws/k8s/haproxy/configure.sh
. ~/k8s/haproxy/configure.sh

vfn=$(mktemp -p /tmp haproxy-${HPX_NAMESPACE}-XXXXXXXXXX)

haproxy_configure "${vfn}" "${envfn}"

helm upgrade --install haproxy-ingress haproxy-ingress \
	--repo https://haproxy-ingress.github.io/charts \
	--namespace "${HPX_NAMESPACE}hpx" \
	--version 0.14.2 \
	--values "${vfn}"

rm -f "${vfn}"
exit 0
