#!/bin/sh
set -eu
# nginx.env
uwskube delete secret proxy-env -n nginx || true
uwskube create secret generic proxy-env -n nginx --from-env-file=${HOME}/cluster/nginx.env
exit 0
