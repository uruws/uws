#!/bin/sh
set -eu
uwskube get all -n meteor-beta
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh
exit 0
