#!/bin/sh
set -eu
ns="infra-ui-${INFRA_UI_ENV}"
export METEOR_NAMESPACE=${ns}
export METEOR_HOST=${INFRA_UI_HOST}
export METEOR_TLS=tapo
exec ~/pod/meteor/gw/restart.sh "${ns}"
