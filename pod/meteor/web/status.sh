#!/bin/sh
set -eu
uwskube get all -n web
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh
exit 0
