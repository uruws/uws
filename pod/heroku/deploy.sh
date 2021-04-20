#!/bin/sh
set -eu

cluster=${UWS_CLUSTER}
kubectl="uwskube ${cluster}"
pod=/home/uws/pod/heroku

appenv=${1:?'app.env?'}

${kubectl} create secret generic heroku-meteor-app-env --from-file="app.env=${appenv}"
${kubectl} apply -f ${pod}/deploy.yaml

exit 0
