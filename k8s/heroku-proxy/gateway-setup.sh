#!/bin/sh
set -eu
envsubst <${HOME}/k8s/heroku-proxy/gateway.yaml | uwskube apply -f -
exit 0
