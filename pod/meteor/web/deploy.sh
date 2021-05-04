#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
pod=/home/uws/pod/meteor/web
uwskube delete secret meteor-web-env || true
uwskube create secret generic meteor-web-env --from-env-file="${appenv}"
uwskube apply -f ${pod}/deploy.yaml
exit 0
