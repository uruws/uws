#!/bin/sh
set -u
uwskube delete secret -n cs appenv
uwskube delete namespace cs
exec ~/pod/meteor/cs/gw/teardown.sh
