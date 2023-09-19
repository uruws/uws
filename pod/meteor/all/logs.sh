#!/bin/sh
set -u
~/pod/meteor/api/logs.sh "$@"
~/pod/meteor/webcdn/logs.sh "$@"
~/pod/meteor/web/logs.sh "$@"
exit 0
