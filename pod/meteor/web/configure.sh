#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
uwskube delete secret -n web meteor-app-env || true
uwskube create secret generic -n web meteor-app-env --from-file="app.env=${appenv}"
exit 0
