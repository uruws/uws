#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
exec ~/pod/lib/scale.sh infra-ui-${INFRA_UI_ENV} meteor "${replicas}"
