#!/bin/sh
set -eu

cluster='amybeta'
kubectl="uwskube ${cluster}"
pod=/home/uws/pod/heroku

appenv=${1:?'app.env?'}

${pod}/deploy.sh ${appenv}

${kubectl} apply -f ${cluster}/meteor-scaler.yaml
${kubectl} apply -f ${cluster}/meteor-gateway.yaml

exit 0
