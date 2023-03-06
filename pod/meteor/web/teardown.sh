#!/bin/sh
set -eu
uwskube delete service meteor -n web
uwskube delete namespace web
~/pod/meteor/web/gw/teardown.sh
exit 0
