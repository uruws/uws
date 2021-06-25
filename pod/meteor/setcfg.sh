#!/bin/sh
set -eu
appver=${1:?'app version?'}
envf=$(mktemp -p /tmp meteor-env.XXXXXXXX)

uwskube delete configmap deploy-env -n meteor || true

echo "export AWS_REGION='${AWS_REGION}'" >${envf}
echo "export METEOR_APP='${appver}'" >>${envf}

uwskube create configmap deploy-env -n meteor --from-file="deploy-env=${envf}"
rm -f ${envf}
exit 0
