#!/bin/sh
set -eu
version=${1:-''}
exec ~/pod/lib/deploy.sh nlpsvc nlpsvc/sentiment/twitter ${version}
