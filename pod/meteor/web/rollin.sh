#!/bin/sh
set -eu
echo 'webcdn'
~/pod/meteor/webcdn/rollin.sh
echo 'web'
uwskube delete deploy meteor -n web
exit 0
