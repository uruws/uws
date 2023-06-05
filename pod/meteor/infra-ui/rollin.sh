#!/bin/sh
set -eu
uwskube delete deploy meteor -n "infra-ui-${INFRA_UI_ENV}"
exit 0
