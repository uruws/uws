#!/bin/sh
set -eu
appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"
uwskube delete secret -n worker meteor-app-env || true
uwskube create secret generic -n worker meteor-app-env --from-file="app.env=${appenv}"
exit 0
