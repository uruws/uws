#!/bin/sh
set -eu

appenv=${HOME}/secret/meteor/infra-ui/${INFRA_UI_ENV}.env
echo "app.env: ${appenv}"

appenv_setup=${HOME}/pod/meteor/app-setup.env
echo "app-setup.env: ${appenv_setup}"

uwskube delete secret -n infra-ui-${INFRA_UI_ENV} appenv || true
uwskube create secret generic -n infra-ui-${INFRA_UI_ENV} appenv \
	--from-file="app.env=${appenv}" \
	--from-file="app-setup.env=${appenv_setup}"

exit 0
