#!/bin/sh
set -eu
exec uwskube create namespace infra-ui-${INFRA_UI_ENV}
