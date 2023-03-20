#!/bin/sh
set -eu

ns=${1:?'namespace?'}
version=${2:?'app version?'}

uwskube delete configmap pod-deploy-env -n "${ns}" || true

envf=$(mktemp -p /tmp pod-${ns}-deploy-env.XXXXXXXX)

echo "export AWS_REGION='${AWS_REGION}'" >${envf}
echo "export APP_VERSION='${version}'" >>${envf}

uwskube create configmap pod-deploy-env -n "${ns}" --from-file="deploy-env=${envf}"
rm -f ${envf}

exit 0
