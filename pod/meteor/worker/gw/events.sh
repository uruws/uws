#!/bin/sh
set -eu
ns=worker
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
