#!/bin/sh
set -eu

#if test "X${INFRA_UI_ENV}" = 'Xtest'; then
#	~/k8s/ca/uws/opstest/setup.sh
#fi

envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml | uwskube apply -f -

./k8s/offline-page/deploy.sh
./k8s/offline-page/setup.sh "infra-ui-${INFRA_UI_ENV}"

exit 0
