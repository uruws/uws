#!/bin/sh
set -u
ns="infra-ui-${INFRA_UI_ENV}"
exec ~/pod/meteor/gw/teardown.sh "${ns}"
