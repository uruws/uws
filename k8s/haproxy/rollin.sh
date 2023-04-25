#!/bin/sh
set -u
prof=${1:?'haproxy profile?'}

envfn="${HOME}/${prof}/haproxy.env"

# shellcheck disable=SC1090
. "${envfn}"

~/k8s/haproxy/ingress/rollin.sh "${prof}"

uwskube delete deploy/haproxy-ingress-default-backend -n "${HPX_NAMESPACE}"
uwskube delete hpa/haproxy-ingress -n "${HPX_NAMESPACE}"
exec uwskube delete deploy/haproxy-ingress -n "${HPX_NAMESPACE}"
