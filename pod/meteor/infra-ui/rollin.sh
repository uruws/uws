#!/bin/sh
set -eu
#~ uwskube delete hpa meteor-hpa -n infra-ui || true
uwskube delete deploy meteor -n infra-ui
exit 0
