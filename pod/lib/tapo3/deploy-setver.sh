#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}
appver=${3:?'app version?'}

uwskube delete configmap "meteor-${app}-deploy" -n "${ns}" || true

uwskube create configmap "meteor-${app}-deploy" -n "${ns}" \
	--from-literal="APP_VERSION=${appver}"

exit 0
