#!/bin/sh
set -eu
appenv=${HOME}/secret/meteor/infra-ui/${INFRA_UI_ENV}.env
echo "app.env: ${appenv}"
uwskube delete secret -n infra-ui-${INFRA_UI_ENV} appenv || true
exec uwskube create secret generic -n infra-ui-${INFRA_UI_ENV} \
	appenv --from-file="app.env=${appenv}"
