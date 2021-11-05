#!/bin/sh
set -eu
version=${1:-''}
~/pod/nlpsvc/configure.sh ${APP_ENV}
exec ~/pod/lib/deploy.sh nlpsvc nlpsvc ${version}
