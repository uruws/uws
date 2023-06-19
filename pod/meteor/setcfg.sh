#!/bin/sh
set -eu

ns=${1:?'app namespace?'}
appver=${2:?'app version?'}
envf=$(mktemp -p /tmp "deploy-meteor-${ns}-env.XXXXXXXX")

# deploy-meteor-env (used internally)

uwskube delete configmap deploy-meteor-env -n "${ns}" || true

echo "export AWS_REGION='${AWS_REGION}'" >"${envf}"
echo "export METEOR_APP='${appver}'" >>"${envf}"

uwskube create configmap deploy-meteor-env -n "${ns}" \
	--from-file="deploy-env=${envf}"
rm -f "${envf}"

# meteor-deploy-env (used for deploy)

envf=$(mktemp -p /tmp "meteor-deploy-${ns}-env.XXXXXXXX")
echo "UWS_APP_ENV=${APP_ENV}" >"${envf}"
if test "X${APP_ENV}" = 'Xstaging'; then
	echo "STAGING_APP_VERSION=${appver}" >>"${envf}"
fi
uwskube delete secret -n "${ns}" meteor-deploy-env || true
uwskube create secret generic -n "${ns}" meteor-deploy-env --from-env-file="${envf}"
rm -vf "${envf}"

exit 0
