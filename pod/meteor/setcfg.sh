#!/bin/sh
set -eu
appver=${1:?'app version?'}
envf=$(mktemp meteor-env.XXXXXXXX)

uwskube delete configmap deploy-env -n meteor || true

echo "METEOR_APP='${appver}'" >${envf}
uwskube create configmap deploy-env -n meteor --from-file="deploy-env=${envf}"
rm -f ${envf}
exit 0
