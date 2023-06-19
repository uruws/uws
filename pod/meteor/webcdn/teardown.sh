#!/bin/sh
set -u
ns=webcdn
~/pod/meteor/gw/teardown.sh "${ns}"
uwskube delete namespace "${ns}"
exit 0
