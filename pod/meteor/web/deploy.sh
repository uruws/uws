#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
pod=/home/uws/pod/meteor/web
uwskube delete secret -n meteor-web meteor-web-env || true
uwskube create secret generic -n meteor-web meteor-web-env --from-file="app.env=${appenv}"
uwskube apply -n meteor-web -f ${pod}/deploy.yaml
exit 0
