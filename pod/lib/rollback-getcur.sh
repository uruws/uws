#!/bin/sh
set -eu
ns=${1:?'namespace?'}

./pod/lib/getcfg.sh "${ns}" |
	fgrep APP_VERSION       |
	sed 's/^export //'      |
	cut -d '=' -f 2         |
	tr -d "'"

exit 0
