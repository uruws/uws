#!/bin/sh
set -eu
uwskube delete deploy meteor -n web
~/pod/meteor/web/cdn/rollin.sh
exit 0
