#!/bin/sh
set -eu
appver=${1:-''}
ns="infra-ui-${INFRA_UI_ENV}"
~/pod/meteor/infra-ui/configure.sh
~/pod/meteor/deploy.sh "${ns}" infra-ui "${appver}"
~/pod/meteor/infra-ui/gw/deploy.sh
exit 0
