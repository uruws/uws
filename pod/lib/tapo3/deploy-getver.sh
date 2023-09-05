#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}

uwskube get configmap "meteor-${app}-deploy" -n "${ns}" \
	-o jsonpath='{.data.APP_VERSION}'

exit 0
