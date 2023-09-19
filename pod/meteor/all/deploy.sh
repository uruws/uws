#!/bin/sh
set -eu
appver=${1:?'app version?'}
~/pod/meteor/api/deploy.sh "${appver}"
~/pod/meteor/web/deploy.sh "${appver}"
~/pod/meteor/api/wait.sh
~/pod/meteor/web/wait.sh
exit 0
