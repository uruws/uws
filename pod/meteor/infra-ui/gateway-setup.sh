#!/bin/sh
set -eu

#if test "X${INFRA_UI_ENV}" = 'Xtest'; then
#	~/k8s/ca/uws/opstest/setup.sh
#fi

envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml | uwskube apply -f -

exit 0
