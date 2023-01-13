#!/bin/sh
set -eu
cat ~/pod/meteor/cs/gateway-${METEOR_CS_ENV}.yaml \
	~/pod/meteor/cs/gateway-common.yaml |
	envsubst | uwskube apply -f -
./k8s/offline-page/deploy.sh
./k8s/offline-page/setup.sh meteor-cs-gateway
exit 0
