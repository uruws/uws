#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
envfn="${HOME}/secret/meteor/cs/${appenv}.env"
uwskube delete secret -n cs appenv || true
uwskube create secret generic -n cs appenv --from-file="app.env=${envfn}"
exit 0
