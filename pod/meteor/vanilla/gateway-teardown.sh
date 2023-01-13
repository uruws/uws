#!/bin/sh
set -eu
envsubst <${HOME}/pod/meteor/vanilla/gateway.yaml | uwskube delete -f -
exit 0
