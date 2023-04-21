#!/bin/sh
set -eu

envfn=${1:?'haproxy env file?'}
ingfn=${2:?'haproxy ingress file?'}

# shellcheck source=/home/uws/k8s/haproxy/ingress/configure.sh
. ~/k8s/haproxy/ingress/configure.sh

haproxy_ingress_configure delete "${envfn}" "${ingfn}"

exit 0
