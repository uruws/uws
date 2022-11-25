#!/bin/sh
set -eu
export METEOR_NAMESPACE=api
exec ~/pod/meteor/web/configure.sh
