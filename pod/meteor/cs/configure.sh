#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
uwskube delete secret -n cs appenv || true
uwskube create secret generic -n cs appenv --from-file="app.env=${appenv}"
exit 0
