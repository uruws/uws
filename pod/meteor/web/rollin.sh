#!/bin/sh
set -eu
uwskube delete deploy meteor -n web
~/pod/meteor/web/gw/rollin.sh
exit 0
