#!/bin/sh
set -eu
exec uwskube get ev -n cert-manager --sort-by=lastTimestamp "$@"
