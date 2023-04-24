#!/bin/sh
set -u
ns=${1:?'haproxy namespace?'}
shift
uwskube delete deploy/haproxy-ingress-default-backend -n "${ns}"
uwskube delete hpa/haproxy-ingress -n "${ns}"
exec uwskube delete deploy/haproxy-ingress -n "${ns}"
