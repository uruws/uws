#!/bin/sh
set -eu
uwskube delete deploy meteor -n cs
exec ~/pod/meteor/cs/gw/rollin.sh
