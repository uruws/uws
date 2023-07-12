#!/bin/sh
set -eu
uwscb_ns=cb${UWSCB_ENV}
exec ~/pod/lib/events.sh "${uwscb_ns}" "$@"
