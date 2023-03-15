#!/bin/sh
set -eu
uwskube delete service   meteor         -n worker
uwskube delete secret    meteor-app-env -n worker
uwskube delete namespace worker
~/pod/meteor/worker/gw/teardown.sh
exit 0
