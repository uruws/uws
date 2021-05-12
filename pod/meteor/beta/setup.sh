#!/bin/sh
set -eu

appenv=${1:?'app.env?'}

uwskube create namespace meteor-beta

uwskube delete secret -n meteor-beta meteor-beta-env || true
uwskube create secret generic -n meteor-beta meteor-beta-env --from-file="app.env=${appenv}"

exit 0
