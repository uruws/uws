#!/bin/sh
set -eu
ns=${1:?'app namespace?'}
app=${2:?'app name?'}
appver=${3:?'app version?'}
envf=$(mktemp -p /tmp meteor-deploy-${app}-env.XXXXXXXX)

uwskube delete configmap deploy-${app}-env -n meteor || true

echo "export AWS_REGION='${AWS_REGION}'" >${envf}
echo "export METEOR_APP='${appver}'" >>${envf}

uwskube create configmap deploy-${app}-env -n meteor --from-file="deploy-env=${envf}"
rm -f ${envf}

if test "X${ns}" = 'Xweb'; then
	envf=$(mktemp -p /tmp meteor-deploy-web-env.XXXXXXXX)
	echo "UWS_APP_ENV=${APP_ENV}" >${envf}
	if test "X${APP_ENV}" = 'Xstaging'; then
		echo "STAGING_APP_VERSION=${appver}" >>${envf}
	fi
	uwskube delete secret -n web meteor-deploy-env || true
	uwskube create secret generic -n web meteor-deploy-env --from-env-file="${envf}"
	rm -vf ${envf}
fi

exit 0
