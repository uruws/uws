#!/bin/sh
set -eu
uwskube delete deploy meteor -n meteor-vanilla
~/pod/meteor/vanilla/gw/rollin.sh
exit 0
