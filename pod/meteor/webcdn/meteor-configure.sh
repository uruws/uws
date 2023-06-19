#!/bin/sh
set -eu
export APP_NAMESPACE=webcdn
exec ~/pod/meteor/web/configure.sh
