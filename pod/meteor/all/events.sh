#!/bin/sh
set -u
~/pod/meteor/api/events.sh "$@"
~/pod/meteor/webcdn/events.sh "$@"
~/pod/meteor/web/events.sh "$@"
exit 0
