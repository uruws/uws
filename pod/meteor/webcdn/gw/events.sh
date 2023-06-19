#!/bin/sh
set -eu
ns=webcdn
exec ~/pod/meteor/gw/events.sh "${ns}" "$@"
