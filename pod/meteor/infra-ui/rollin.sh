#!/bin/sh
set -eu
exec uwskube delete deploy meteor -n infra-ui-${INFRA_UI_ENV}
