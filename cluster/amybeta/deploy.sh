#!/bin/sh
set -eu

pod=/home/uws/pod/heroku
cluster=/home/uws/cluster/amybeta

appenv=${1:?'app.env?'}
${pod}/deploy.sh ${appenv}

uwskube apply -f ${cluster}/meteor-gateway.yaml

exit 0
