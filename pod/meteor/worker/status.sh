#!/bin/sh
set -eu
uwskube get deploy,rs,hpa -n worker
echo
echo 'DEPLOY ENV'
~/pod/meteor/getcfg.sh
exit 0
