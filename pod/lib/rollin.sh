#!/bin/sh
set -u
ns=${1:?'namespace?'}
app=${2:?'app name?'}
pod=${HOME}/pod/${app}
envsubst <${pod}/deploy.yaml | uwskube delete -n "${ns}" -f -
exit 0
