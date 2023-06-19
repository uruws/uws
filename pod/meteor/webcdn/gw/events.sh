#!/bin/sh
set -eu
ns=webcdn
exec ~/pod/lib/events.sh "${ns}" "$@"
