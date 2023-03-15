#!/bin/sh
set -u
uwskube delete secret -n meteor-vanilla appenv
uwskube delete service meteor -n meteor-vanilla
uwskube delete namespace meteor-vanilla
~/pod/meteor/vanilla/gw/teardown.sh
exit 0
