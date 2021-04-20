#!/bin/sh
set -eu

cluster=${UWS_CLUSTER}
kubectl="uwskube ${cluster}"
pod=/home/uws/pod/heroku

${kubectl} delete -f ${pod}/deploy.yaml
${kubectl} delete secret heroku-meteor-app-env

exit 0
