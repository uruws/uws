#!/bin/sh
set -eu
uwskube delete deploy meteor -n "infra-ui-${INFRA_UI_ENV}"
~/pod/meteor/infra-ui/gw/rollin.sh
exit 0
