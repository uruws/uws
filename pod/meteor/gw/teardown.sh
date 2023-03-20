#!/bin/sh
set -u
ns="${1:?'namespace?'}gw"
~/k8s/nginx/teardown.sh "${ns}"
exec uwskube delete namespace "${ns}"
