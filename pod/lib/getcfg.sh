#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube get configmap pod-deploy-env -n "${ns}" -o jsonpath='{.data.deploy-env}'
