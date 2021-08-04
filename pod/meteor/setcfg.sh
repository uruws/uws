#!/bin/sh
set -eu
app=${1:?'app name?'}
appver=${2:?'app version?'}
envf=$(mktemp -p /tmp meteor-deploy-${app}-env.XXXXXXXX)

uwskube delete configmap deploy-${app}-env -n meteor || true

echo "export AWS_REGION='${AWS_REGION}'" >${envf}
echo "export METEOR_APP='${appver}'" >>${envf}

uwskube create configmap deploy-${app}-env -n meteor --from-file="deploy-env=${envf}"
rm -f ${envf}
exit 0
