#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
uwskube delete secret -n meteor-web meteor-web-env || true
uwskube create secret generic -n meteor-web meteor-web-env --from-file="app.env=${appenv}"
exit 0
