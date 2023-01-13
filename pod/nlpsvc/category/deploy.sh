#!/bin/sh
set -eu
version=${1:-''}
~/pod/nlpsvc/configure.sh "${NLPSVC_ENV}"
exec ~/pod/lib/deploy.sh nlpsvc nlpsvc/category ${version}
