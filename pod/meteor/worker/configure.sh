#!/bin/sh
set -eu

appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"

appset=${HOME}/secret/meteor/app/${APP_ENV}-settings.json
echo "app-settings.json: ${appset}"

uwskube delete secret -n worker meteor-app-env || true

if test -s "${appset}"; then
	uwskube create secret generic -n worker meteor-app-env \
		--from-file="app.env=${appenv}" \
		--from-file="app-settings.json=${appset}"
else
	uwskube create secret generic -n worker meteor-app-env \
		--from-file="app.env=${appenv}"
fi

exit 0
