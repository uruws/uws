#!/bin/sh
set -eu
envsubst <${HOME}/k8s/heroku-proxy/gateway.yaml | uwskube apply -f -
~/k8s/offline-page/deploy.sh
~/k8s/offline-page/setup.sh heroku-staging
exit 0
