#!/bin/sh
set -eu
${HOME}/k8s/nginx/configure.sh
exec uwskube rollout restart deployment proxy -n nginx
