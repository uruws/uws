#!/bin/sh
set -eu

ns=${1:?'namespace?'}
app=${2:?'app name?'}

appenv=${HOME}/secret/meteor/app/${TAPO_ENV}.env

uwskube delete secret "meteor-${app}-env" -n "${ns}" || true

if test -s "${appenv}"; then
	appset=${HOME}/secret/meteor/app/${TAPO_ENV}-settings.json

	echo "app.env: ${appenv}"
	echo "app-settings.json: ${appset}"

	envfn=$(mktemp -p /tmp "configure-${ns}-${app}-env.XXXXXXXXXX")

	cat "${appenv}" >"${envfn}"

	echo -n 'METEOR_SETTINGS=' >>"${envfn}"
	python3 -m json.tool --compact "${appset}" >>"${envfn}"

	if test 'Xworker' != "X${app}"; then
		echo 'DISABLE_JOBS=TRUE' >>"${envfn}"
	fi

	uwskube create secret generic "meteor-${app}-env" -n "${ns}" --from-env-file="${envfn}"
	rm -vf "${envfn}"
fi

exit 0
