#!/bin/sh
set -eu
uwskube create namespace cs
exec ~/pod/meteor/cs/gw/setup.sh
