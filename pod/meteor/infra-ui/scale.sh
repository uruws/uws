#!/bin/sh
set -eu
replicas=${1:?'replicas?'}
~/pod/lib/scale.sh "infra-ui-${INFRA_UI_ENV}" meteor "${replicas}"
exit 0
