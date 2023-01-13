#!/bin/sh
set -eu
appenv=${HOME}/secret/meteor/vanilla/${METEOR_VANILLA_ENV}.env
echo "app.env: ${appenv}"
uwskube delete secret -n meteor-vanilla appenv || true
exec uwskube create secret generic -n meteor-vanilla \
	appenv --from-file="app.env=${appenv}"
