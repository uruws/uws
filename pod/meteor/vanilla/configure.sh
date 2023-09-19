#!/bin/sh
set -eu

appenv=${HOME}/secret/meteor/vanilla/${METEOR_VANILLA_ENV}.env
echo "app.env: ${appenv}"

appenv_setup=${HOME}/pod/meteor/app-setup.env
echo "app-setup.env: ${appenv_setup}"

uwskube delete secret -n meteor-vanilla appenv || true
uwskube create secret generic -n meteor-vanilla appenv \
	--from-file="app.env=${appenv}" \
	--from-file="app-setup.env=${appenv_setup}"

exit 0
