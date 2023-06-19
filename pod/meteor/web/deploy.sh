#!/bin/sh
set -eu
appver=${1:-''}

~/pod/meteor/webcdn/deploy.sh "${appver}"
~/pod/meteor/webcdn/wait.sh

~/pod/meteor/web/configure.sh
exec ~/pod/meteor/deploy.sh web web "${appver}"
