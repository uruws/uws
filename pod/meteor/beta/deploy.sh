#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
pod=/home/uws/pod/meteor/beta
uwskube delete secret -n meteor-beta meteor-beta-env || true
uwskube create secret generic -n meteor-beta meteor-beta-env --from-file="app.env=${appenv}"
uwskube apply -n meteor-beta -f ${pod}/deploy.yaml
exit 0
