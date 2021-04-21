#!/bin/sh
set -eu

kubectl='uwskube amybeta'
pod=/home/uws/pod/heroku
cluster=/home/uws/cluster/amybeta

appenv=${1:?'app.env?'}

${pod}/deploy.sh ${appenv}

${kubectl} apply -f ${cluster}/meteor-scaler.yaml
${kubectl} apply -f ${cluster}/meteor-gateway.yaml

exit 0
