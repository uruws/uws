#!/bin/sh
set -eu
ns=webcdn
exec ~/pod/lib/status.sh "${ns}" all "$@"
