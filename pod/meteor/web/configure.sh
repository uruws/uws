#!/bin/sh
set -eu

NS=${APP_NAMESPACE:-web}

appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"

appset=${HOME}/secret/meteor/app/${APP_ENV}-settings.json
echo "app-settings.json: ${appset}"

uwskube delete secret -n "${NS}" meteor-app-env || true

if test -s "${appset}"; then
	uwskube create secret generic -n "${NS}" meteor-app-env \
		--from-file="app.env=${appenv}" \
		--from-file="app-settings.json=${appset}"
else
	uwskube create secret generic -n "${NS}" meteor-app-env \
		--from-file="app.env=${appenv}"
fi

exit 0
