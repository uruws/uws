#!/bin/sh
set -eu
uwskube delete hpa worker-hpa -n worker
uwskube delete deploy meteor -n worker
exit 0
