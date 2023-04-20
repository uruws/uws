#!/bin/sh
set -eu
ns="${1:?'haproxy namespace?'}hpx"
shift
exec uwskube rollout restart deployment/haproxy-ingress-default-backend -n "${ns}"
