#!/bin/sh
set -eu

appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"

appenv_cluster=${HOME}/secret/meteor/app/${UWS_CLUSTER}.env
echo "app-cluster.env: ${appenv_cluster}"

appset=${HOME}/secret/meteor/app/${APP_ENV}-settings.json
echo "app-settings.json: ${appset}"

uwskube delete secret -n worker meteor-app-env || true

uwskube create secret generic -n worker meteor-app-env \
	--from-file="app.env=${appenv}" \
	--from-file="app-cluster.env=${appenv_cluster}" \
	--from-file="app-settings.json=${appset}"

exit 0
