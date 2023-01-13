#!/bin/sh
set -u
envsubst <${HOME}/pod/meteor/infra-ui/gateway.yaml | uwskube delete -f -
uwskube delete secret -n infra-ui-${INFRA_UI_ENV} appenv || true
exec uwskube delete namespace infra-ui-${INFRA_UI_ENV}
