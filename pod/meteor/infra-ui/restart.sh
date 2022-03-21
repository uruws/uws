#!/bin/sh
set -eu
exec uwskube rollout restart deployment -n infra-ui-${INFRA_UI_ENV}
