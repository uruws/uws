#!/bin/sh
set -eu
appver=${1:-''}
ns="infra-ui-${INFRA_UI_ENV}"

~/pod/meteor/infra-ui/configure.sh

export APP_ENV="${INFRA_UI_ENV}"
~/pod/meteor/deploy.sh "${ns}" infra-ui "${appver}"

exit 0
