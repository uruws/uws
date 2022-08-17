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

clusterenv=${HOME}/secret/meteor/app/${APP_ENV}-${UWS_CLUSTER}.env
echo "cluster.env: ${clusterenv}"

uwskube delete secret -n worker meteor-cluster-env || true

uwskube create secret generic -n worker meteor-cluster-env \
	--from-file="meteor-app.env=${clusterenv}"

exit 0
