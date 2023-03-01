#!/bin/sh
set -eu
ns="${1:?'namespace?'}gw"
uwskube create namespace "${ns}"
exec ~/k8s/nginx/setup.sh "${ns}"
