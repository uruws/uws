#!/bin/sh
set -eu
envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml | uwskube delete -f -
exit 0
