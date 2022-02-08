#!/bin/sh
set -eu
version=${1:-''}
exec ~/pod/lib/deploy.sh uwspod podtest ${version}
