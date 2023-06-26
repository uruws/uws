#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/webcdn/configure.sh
export APP_REPLICAS=${APPCDN_REPLICAS}
~/pod/meteor/deploy.sh webcdn web "${appver}"
exit 0
