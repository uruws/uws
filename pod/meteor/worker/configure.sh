#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
uwskube delete secret -n worker meteor-app-env || true
uwskube create secret generic -n worker meteor-app-env --from-file="app.env=${appenv}"
exit 0
