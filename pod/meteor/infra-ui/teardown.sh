#!/bin/sh
set -eu
uwskube delete -f ~/pod/meteor/infra-ui/gateway.yaml || true
uwskube delete secret -n infra-ui-${INFRA_UI_ENV} appenv || true
exec uwskube delete namespace infra-ui-${INFRA_UI_ENV}
