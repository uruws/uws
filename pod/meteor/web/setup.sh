#!/bin/sh
set -eu
uwskube create namespace web
~/pod/meteor/web/gw/setup.sh
exit 0
