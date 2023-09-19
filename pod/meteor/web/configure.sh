#!/bin/sh
set -eu

NS=${APP_NAMESPACE:-web}

appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"

appenv_setup=${HOME}/pod/meteor/app-setup.env
echo "app-setup.env: ${appenv_setup}"

appset=${HOME}/secret/meteor/app/${APP_ENV}-settings.json
echo "app-settings.json: ${appset}"

uwskube delete secret -n "${NS}" meteor-app-env || true

uwskube create secret generic -n "${NS}" meteor-app-env \
	--from-file="app.env=${appenv}" \
	--from-file="app-setup.env=${appenv_setup}" \
	--from-file="app-settings.json=${appset}"

exit 0
