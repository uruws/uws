#!/bin/sh
set -eu

appenv=${1:?'app.env?'}

pod=/home/uws/pod/heroku

uwskube delete secret heroku-meteor-app-env || true
uwskube create secret generic heroku-meteor-app-env --from-file="app.env=${appenv}"
uwskube apply -f ${pod}/deploy.yaml

exit 0
