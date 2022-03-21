#!/bin/sh
set -eu
uwskube create namespace infra-ui-${INFRA_UI_ENV}
exec ~/pod/meteor/infra-ui/gateway-setup.sh
