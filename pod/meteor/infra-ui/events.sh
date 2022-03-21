#!/bin/sh
set -eu
exec ~/pod/lib/events.sh infra-ui-${INFRA_UI_ENV} "$@"
