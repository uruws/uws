#!/bin/sh
set -eu
ns=${1:?'haproxy namespace?'}
shift
exec ~/pod/lib/top.sh "${ns}" -l 'app.kubernetes.io/name=haproxy-ingress'
