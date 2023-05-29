#!/bin/sh
set -eu

NS=${APP_NAMESPACE:-web}

appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"

appenv_cluster=${HOME}/secret/meteor/app/${UWS_CLUSTER}.env
if ! test -s "${appenv_cluster}"; then
	appenv_cluster=${HOME}/secret/meteor/app/empty.env
fi
echo "app-cluster.env: ${appenv_cluster}"

appset=${HOME}/secret/meteor/app/${APP_ENV}-settings.json
echo "app-settings.json: ${appset}"

uwskube delete secret -n "${NS}" meteor-app-env || true

uwskube create secret generic -n "${NS}" meteor-app-env \
	--from-file="app.env=${appenv}" \
	--from-file="app-cluster.env=${appenv_cluster}" \
	--from-file="app-settings.json=${appset}"

exit 0
