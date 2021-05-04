#!/bin/sh
set -eu
appenv=${1:?'app.env?'}
pod=/home/uws/pod/meteor/worker
uwskube delete secret -n meteor-worker meteor-worker-env || true
uwskube create secret generic -n meteor-worker meteor-worker-env --from-file="app.env=${appenv}"
uwskube apply -n meteor-worker -f ${pod}/deploy.yaml
exit 0
