#!/bin/sh
set -eu
${HOME}/pod/meteor/infra-ui/configure.sh
exec uwskube rollout restart deployment -n infra-ui-${INFRA_UI_ENV}
