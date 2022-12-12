#!/bin/sh
set -eu
uwskube create namespace meteor-vanilla
exec ~/pod/meteor/vanilla/gateway-setup.sh
