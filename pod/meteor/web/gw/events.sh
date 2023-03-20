#!/bin/sh
set -eu
ns=web
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
