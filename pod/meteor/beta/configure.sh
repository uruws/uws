#!/bin/sh
set -eu
appenv=${HOME}/secret/meteor/app/${APP_ENV}.env
echo "app.env: ${appenv}"
uwskube delete secret -n meteor-beta meteor-beta-env || true
uwskube create secret generic -n meteor-beta meteor-beta-env --from-file="app.env=${appenv}"
exit 0
