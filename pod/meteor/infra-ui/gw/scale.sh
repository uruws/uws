#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
ns="infra-ui-${INFRA_UI_ENV}"
exec ~/pod/meteor/gw/scale.sh "${ns}" "${replicas}"
