#!/bin/sh
set -eu
ns="infra-ui-${INFRA_UI_ENV}"
export METEOR_NAMESPACE=${ns}
export METEOR_TLS=tapo
export METEOR_HOST=${INFRA_UI_HOST}
export NGINX_REPLICAS=${INFRA_UI_REPLICAS}
exec ~/pod/meteor/gw/deploy.sh "${ns}"
