#!/bin/sh
set -eu
appenv=${HOME}/secret/meteor/infra-ui/${INFRA_UI_ENV}.env
echo "app.env: ${appenv}"
uwskube delete secret -n infra-ui appenv || true
uwskube create secret generic -n infra-ui appenv --from-file="app.env=${appenv}"
exit 0
