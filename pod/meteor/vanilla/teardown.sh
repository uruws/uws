#!/bin/sh
set -u
envsubst <${HOME}/pod/meteor/vanilla/gateway.yaml | uwskube delete -f -
uwskube delete secret -n meteor-vanilla appenv || true
exec uwskube delete namespace meteor-vanilla
