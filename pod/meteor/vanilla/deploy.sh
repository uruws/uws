#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/vanilla/configure.sh
~/pod/meteor/deploy.sh meteor-vanilla vanilla "${appver}"
~/pod/meteor/vanilla/gw/deploy.sh
exit 0
