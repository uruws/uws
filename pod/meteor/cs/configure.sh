#!/bin/sh
set -eu
appenv=${1:?'app.env?'}

envfn="${HOME}/secret/meteor/cs/${appenv}.env"
appenv_setup=${HOME}/pod/meteor/app-setup.env

uwskube delete secret -n cs appenv || true
uwskube create secret generic -n cs appenv \
	--from-file="app.env=${envfn}" \
	--from-file="app-setup.env=${appenv_setup}"

exit 0
