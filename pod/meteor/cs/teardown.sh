#!/bin/sh
set -u
uwskube delete secret    appenv -n cs
uwskube delete service   meteor -n cs
uwskube delete namespace cs
exec ~/pod/meteor/cs/gw/teardown.sh
