#!/bin/sh
set -eu
uwskube delete hpa web-hpa -n web || true
uwskube delete deploy meteor -n web
exit 0
