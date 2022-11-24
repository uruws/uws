#!/bin/sh
set -eu
envsubst <${HOME}/k8s/heroku-proxy/gateway.yaml | uwskube delete -f -
exit 0
