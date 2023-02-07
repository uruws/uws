#!/bin/sh
set -eu

NGINX_VERSION=$(cat ~/k8s/nginx/VERSION)
export NGINX_VERSION

envsubst <~/k8s/nginx/deploy.yaml | uwskube apply -n nginx -f -

exit 0
