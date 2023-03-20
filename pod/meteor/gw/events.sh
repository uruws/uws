#!/bin/sh
set -eu
ns="${1:?'namespace?'}gw"
shift
exec ~/k8s/nginx/events.sh "${ns}" "$@"
