#!/bin/sh
set -eu
~/pod/meteor/infra-ui/configure.sh
uwskube rollout restart deployment -n "infra-ui-${INFRA_UI_ENV}"
~/pod/meteor/infra-ui/gw/restart.sh
exit 0
