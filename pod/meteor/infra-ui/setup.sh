#!/bin/sh
set -eu
ns="infra-ui-${INFRA_UI_ENV}"
uwskube create namespace "${ns}"
exit 0
