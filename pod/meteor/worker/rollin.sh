#!/bin/sh
set -eu
uwskube delete deploy meteor -n worker
~/pod/meteor/worker/gw/rollin.sh
exit 0
