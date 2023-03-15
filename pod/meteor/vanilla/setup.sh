#!/bin/sh
set -eu
uwskube create namespace meteor-vanilla
~/pod/meteor/vanilla/gw/setup.sh
exit 0
