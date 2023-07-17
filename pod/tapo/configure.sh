#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}
appver=${3:-NO_VERSION}

appenv=${HOME}/secret/meteor/app/${TAPO_ENV}.env

uwskube delete secret app-env -n "${ns}" || true
uwskube create secret generic app-env -n "${ns}" \
	--from-file="app.env=${HOME}/secret/meteor/app/empty.env"

uwskube delete secret "meteor-${app}-env" -n "${ns}" || true

if test 'XNO_VERSION' = "X${appver}"; then
	appver=$(~/pod/tapo/deploy-getver.sh "${ns}" "${app}")
fi

if test -s "${appenv}"; then
	appset=${HOME}/secret/meteor/app/${TAPO_ENV}-settings.json

	echo "app.env: ${appenv}"
	echo "app-settings.json: ${appset}"

	envfn=$(mktemp -p /tmp "configure-${ns}-${app}-env.XXXXXXXXXX")

	cat "${appenv}" >"${envfn}"

	printf '%s' 'METEOR_SETTINGS=' >>"${envfn}"
	python3 -m json.tool --compact "${appset}" >>"${envfn}"

	if test 'Xworker' != "X${app}"; then
		echo 'DISABLE_JOBS=TRUE' >>"${envfn}"
	fi

	if test 'Xprod' != "X${TAPO_ENV}"; then
		echo "STAGING_APP_VERSION=${appver}" >>"${envfn}"
	fi

	uwskube create secret generic "meteor-${app}-env" -n "${ns}" --from-env-file="${envfn}"
	rm -vf "${envfn}"
fi

exit 0
