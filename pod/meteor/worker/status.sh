#!/bin/sh
set -eu
uwskube get all -n worker
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh
exit 0
