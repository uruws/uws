#!/bin/sh
set -eu
uwskube create namespace worker
~/pod/meteor/worker/gw/setup.sh
exit 0
