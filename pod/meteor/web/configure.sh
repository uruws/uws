#!/bin/sh
set -eu
ns=${1:?'namespace?'}
appenv=${2:?'app.env?'}
uwskube delete secret -n ${ns} meteor-app-env || true
uwskube create secret generic -n web meteor-app-env --from-file="app.env=${appenv}"
exit 0
