#!/bin/sh
set -eu
export APP_NAMESPACE=api
exec ~/pod/meteor/web/configure.sh
