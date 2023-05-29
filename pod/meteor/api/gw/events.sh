#!/bin/sh
set -eu
ns=api
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
