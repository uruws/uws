#!/bin/sh
set -eu
exec uwskube get ev -A --sort-by=lastTimestamp "$@"
