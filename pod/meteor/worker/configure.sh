#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
uwskube delete secret -n meteor-worker meteor-worker-env || true
uwskube create secret generic -n meteor-worker meteor-worker-env --from-file="app.env=${appenv}"
exit 0
