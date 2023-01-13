#!/bin/sh
set -eu
uwskube delete hpa web-hpa -n api || true
uwskube delete deploy meteor -n api
exit 0
