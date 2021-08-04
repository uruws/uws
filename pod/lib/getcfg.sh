#!/bin/sh
set -eu
ns=${1:?'namespace?'}
uwskube get configmap pod-deploy-env -n ${ns} -o jsonpath='{.data.deploy-env}'
exit 0
