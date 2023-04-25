#!/bin/sh
set -eu

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

# shellcheck source=/home/uws/k8s/haproxy/configure.sh
. ~/k8s/haproxy/configure.sh

vfn=$(mktemp -p /tmp haproxy-${HPX_NAMESPACE}-install-XXXXXXXXXX)

haproxy_configure "${vfn}" "${prof}"

rm -f "${vfn}"

exec ~/k8s/haproxy/ingress/deploy.sh "${prof}"
