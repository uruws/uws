#!/bin/sh
set -eu
uwskube get all -n web
echo
echo 'DEPLOY CONFIG'
~/pod/meteor/getcfg.sh
exit 0
