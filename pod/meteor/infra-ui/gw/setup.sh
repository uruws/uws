#!/bin/sh
set -eu
ns="infra-ui-${INFRA_UI_ENV}"
exec ~/pod/meteor/gw/setup.sh "${ns}"
