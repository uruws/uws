#!/bin/sh
set -eu
~/k8s/ca/uws/opstest/setup.sh
envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml | uwskube apply -f -
exit 0
