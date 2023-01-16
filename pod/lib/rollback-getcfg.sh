#!/bin/sh
set -eu
ns=${1:?'namespace?'}
exec uwskube get configmap pod-deploy-rollback -n "${ns}" -o jsonpath='{.data.deploy-rollback}'
