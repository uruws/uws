#!/bin/sh
set -eu
~/pod/meteor/webcdn/rollin.sh
uwskube delete deploy meteor -n web
exit 0
