#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
exec uwskube get configmap "deploy-${app}-env" -n "${ns}" \
	-o jsonpath='{.data.deploy-env}'
