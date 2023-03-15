#!/bin/sh
set -eu
ns=cs
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
