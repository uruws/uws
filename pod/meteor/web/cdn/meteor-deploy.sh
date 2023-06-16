#!/bin/sh
set -eu
appver=${1:-''}
~/pod/meteor/web/cdn/meteor-configure.sh
export APP_REPLICAS=${APPCDN_METEOR_REPLICAS}
~/pod/meteor/deploy.sh webcdn web "${appver}"
exit 0
