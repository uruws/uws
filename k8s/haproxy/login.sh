#!/bin/sh
set -eu
ns=${1:?'haproxy namespace?'}
shift
exec uwskube exec deploy/haproxy-ingress -n "${ns}" -it -c haproxy-ingress -- /bin/sh -il
