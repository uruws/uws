#!/bin/sh
set -eu
ns=${1:?'haproxy namespace?'}
shift
exec uwskube get all -n "${ns}" -l 'app.kubernetes.io/name=haproxy-ingress'
