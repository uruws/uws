#!/bin/sh
set -eu
pod=/home/uws/pod/heroku
cluster=/home/uws/cluster/amybeta

uwskube delete -f ${cluster}/meteor-gateway.yaml
uwskube delete -f ${cluster}/meteor-scaler.yaml

${pod}/teardown.sh
exit 0
