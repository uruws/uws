#!/bin/sh
set -eu

prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"
ingfn="${HOME}/${prof}/ingress.yaml"

# shellcheck source=/home/uws/k8s/haproxy/ingress/configure.sh
. ~/k8s/haproxy/ingress/configure.sh

haproxy_ingress_configure delete "${envfn}" "${ingfn}"

exit 0
