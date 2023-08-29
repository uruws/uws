#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}
appver=${3:-NO_VERSION}

appenv=${HOME}/secret/meteor/app/${TAPO_ENV}.env

if test 'XNO_VERSION' = "X${appver}"; then
	appver=$(~/pod/tapo/deploy-getver.sh "${ns}" "${app}")
fi

# remove old
uwskube delete secret app-env -n "${ns}" || true
uwskube delete secret empty-app-env -n "${ns}" || true

#-------------------------------------------------------------------------------
# meteor env

if test -s "${appenv}"; then
	echo "app.env: ${appenv}"
	uwskube delete secret "meteor-${app}-env" -n "${ns}" || true
	uwskube create secret generic "meteor-${app}-env" -n "${ns}" \
		--from-file="${appenv}"
else
	echo "[ERROR] ${appenv}: file not found or empty!" >&2
	exit 1
fi

#-------------------------------------------------------------------------------
# deploy env

uwskube delete secret "deploy-${app}-env" -n "${ns}" || true

appset=${HOME}/secret/meteor/app/${TAPO_ENV}-settings.json

echo "app-settings.json: ${appset}"

envfn=$(mktemp -p /tmp "configure-${ns}-${app}-env.XXXXXXXXXX")

printf '%s' 'METEOR_SETTINGS=' >"${envfn}"
python3 -m json.tool --compact "${appset}" >>"${envfn}"

if test 'Xworker' != "X${app}"; then
	echo 'DISABLE_JOBS=TRUE' >>"${envfn}"
fi

if test 'Xstaging' = "X${TAPO_ENV}"; then
	echo "STAGING_APP_VERSION=${appver}" >>"${envfn}"
fi
if test 'Xsrmnt' = "X${TAPO_ENV}"; then
	echo "STAGING_APP_VERSION=${appver}" >>"${envfn}"
fi
if test 'Xsrmnt-ngx' = "X${TAPO_ENV}"; then
	echo "STAGING_APP_VERSION=${appver}" >>"${envfn}"
fi

uwskube create secret generic "deploy-${app}-env" -n "${ns}" \
	--from-env-file="${envfn}"
rm -vf "${envfn}"

exit 0
