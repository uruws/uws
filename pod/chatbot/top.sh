#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}
exec ~/pod/lib/top.sh "${uwscb_ns}" "$@"
