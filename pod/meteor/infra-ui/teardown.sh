#!/bin/sh
set -u
ns="infra-ui-${INFRA_UI_ENV}"
uwskube delete secret -n "${ns}" appenv || true
uwskube delete namespace "${ns}"
exec ~/pod/meteor/infra-ui/gw/teardown.sh
