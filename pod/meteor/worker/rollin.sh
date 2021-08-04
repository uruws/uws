#!/bin/sh
set -eu
uwskube delete hpa worker-hpa -n worker || true
uwskube delete deploy meteor -n worker
exit 0
